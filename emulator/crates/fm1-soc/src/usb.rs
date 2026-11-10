//! Guru-600: USB0 as the FM-1's firmware drives it (Felucca's src/usb.c and hal/fm1_usb.h), with a host behind it,
//! so a computer's MIDI program (the Guru-600 editor) talks to the emulated FM-1 as to the real one over its cable.
//! Only what a USB-MIDI device needs:
//!   * the SIE: the MUSB byte registers reached through CON1 (0x11804: r << 8 | value, bit 14 a read, bit 15 done
//!     at once), INDEX, CSR0 / COUNT0, EP1's TXCSR1 / RXCSR1 / RXCOUNT, the interrupt flags (cleared when read),
//!     the frame number;
//!   * EP DMA: the buffers are the firmware's own RAM (EP0_ADR, EP1's TADR / RADR, the EP1 count register);
//!   * a host: once the firmware pulls D+ up, a bus reset, then SET_ADDRESS and SET_CONFIGURATION 1 (no
//!     descriptor is asked for: the host knows the device), then EP1 OUT packets from `out_q` and EP1 IN packets to
//!     `in_q` (USB-MIDI event packets, 4 bytes each).
//! The host steps each time the firmware reads INTRUSB (its usb_poll, 2 kHz).

use std::collections::VecDeque;
use fm1_core::Bus;

pub const CON0: u32 = 0x11800;
pub const CON1: u32 = 0x11804;
const EP_CNT1: u32 = 0x1180c;
const EP0_ADR: u32 = 0x11818;
const EP1_TADR: u32 = 0x1181c;
const EP1_RADR: u32 = 0x11820;
const IO_CON0: u32 = 0x51000;

#[derive(Default, Clone, Copy, PartialEq)]
enum Host {
    #[default]
    Detached,
    Reset,
    Address,
    WaitAddress,
    Config,
    WaitConfig,
    Configured,
}

#[derive(Default)]
pub struct Usb {
    host: Host,
    index: u8,
    faddr: u8,
    csr0: u8,
    count0: u8,
    txcsr1: [u8; 5],
    rxcsr1: [u8; 5],
    rxcount: [u8; 5],
    intr_usb: u8,
    intr_tx: u8,
    intr_rx: u8,
    frame: u16,
    polls: u32,
    /// USB-MIDI event packets the host sends (EP1 OUT), 4 bytes each
    pub out_q: VecDeque<u8>,
    /// USB-MIDI event packets the device sent (EP1 IN), for the host's program
    pub in_q: Vec<u8>,
}

impl Usb {
    /// The device is configured: the host's program can talk to it.
    pub fn ready(&self) -> bool {
        self.host == Host::Configured
    }
}

impl super::Soc {
    /// A write of CON1: one SIE access (read or write), done at once.
    pub(crate) fn usb_sie(&mut self, v: u32) {
        let r = ((v >> 8) & 0x3f) as u8;
        let mut out = v & !0xff;
        if v & 0x4000 != 0 {
            out |= self.usb_sie_read(r) as u32;
        } else {
            self.usb_sie_write(r, v as u8);
        }
        self.sfr_set(CON1, out | 0x8000);
    }

    fn usb_sie_read(&mut self, r: u8) -> u8 {
        let i = (self.usb.index as usize).min(4);
        match r {
            0 => self.usb.faddr,
            2 => std::mem::take(&mut self.usb.intr_tx),
            4 => std::mem::take(&mut self.usb.intr_rx),
            6 => {
                self.usb_host();
                std::mem::take(&mut self.usb.intr_usb)
            }
            12 => self.usb.frame as u8,
            13 => (self.usb.frame >> 8) as u8 & 7,
            14 => self.usb.index,
            17 => if i == 0 { self.usb.csr0 } else { self.usb.txcsr1[i] },
            20 => self.usb.rxcsr1[i],
            22 => if i == 0 { self.usb.count0 } else { self.usb.rxcount[i] },
            _ => 0,
        }
    }

    fn usb_sie_write(&mut self, r: u8, v: u8) {
        let i = (self.usb.index as usize).min(4);
        match r {
            0 => self.usb.faddr = v & 0x7f,
            14 => self.usb.index = v & 15,
            17 if i == 0 => {
                // CSR0: ServicedRxPktRdy (0x40) takes the SETUP; TxPktRdy (0x02, an IN data stage) goes at once
                if v & 0x40 != 0 {
                    self.usb.csr0 &= !0x01;
                }
                if v & 0x02 != 0 {
                    self.usb.intr_tx |= 1;
                }
            }
            17 => {
                // TXCSR1: TxPktRdy: the host takes the packet the EP's DMA points at
                if v & 0x01 != 0 && i == 1 {
                    let (a, n) = (self.sfr_get(EP1_TADR), self.sfr_get(EP_CNT1).min(64));
                    for k in 0..n {
                        let b = self.read8(a + k);
                        self.usb.in_q.push(b);
                    }
                    self.usb.intr_tx |= 2;
                }
                self.usb.txcsr1[i] = v & !0x01;
            }
            20 => {
                // RXCSR1: FlushFIFO (0x10, with RxPktRdy left) frees the buffer for the next packet
                self.usb.rxcsr1[i] = if v & 0x10 != 0 { v & !0x11 } else { v };
            }
            _ => {}
        }
    }

    /// The host, one step per usb_poll.
    fn usb_host(&mut self) {
        self.usb.polls = self.usb.polls.wrapping_add(1);
        if self.usb.polls % 2 == 0 {
            self.usb.frame = (self.usb.frame + 1) & 0x7ff;   // (1 ms frames: the firmware sees a live host)
        }
        let attached = self.sfr_get(CON0) & 1 != 0 && self.sfr_get(IO_CON0) & 0x40 != 0;
        if !attached {
            self.usb.host = Host::Detached;
            return;
        }
        match self.usb.host {
            Host::Detached => {
                self.usb.host = Host::Reset;
            }
            Host::Reset => {
                self.usb.intr_usb |= 0x04;
                self.usb.csr0 = 0;
                self.usb.rxcsr1 = [0; 5];
                self.usb.host = Host::Address;
            }
            Host::Address => self.usb_setup([0x00, 0x05, 0x01, 0, 0, 0, 0, 0], Host::WaitAddress),
            Host::WaitAddress if self.usb.csr0 & 1 == 0 => self.usb.host = Host::Config,
            Host::Config => self.usb_setup([0x00, 0x09, 0x01, 0, 0, 0, 0, 0], Host::WaitConfig),
            Host::WaitConfig if self.usb.csr0 & 1 == 0 => self.usb.host = Host::Configured,
            Host::Configured => {
                // EP1 OUT: up to 16 event packets at once, when the device took the last ones
                if self.usb.rxcsr1[1] & 1 == 0 && self.usb.out_q.len() >= 4 {
                    let a = self.sfr_get(EP1_RADR);
                    let n = (self.usb.out_q.len() / 4).min(16) * 4;
                    for k in 0..n as u32 {
                        let b = self.usb.out_q.pop_front().unwrap_or(0);
                        self.write8(a + k, b);
                    }
                    self.usb.rxcount[1] = n as u8;
                    self.usb.rxcsr1[1] |= 1;
                    self.usb.intr_rx |= 2;
                }
            }
            _ => {}
        }
    }

    fn usb_setup(&mut self, s: [u8; 8], next: Host) {
        let a = self.sfr_get(EP0_ADR);
        for (k, b) in s.iter().enumerate() {
            self.write8(a + k as u32, *b);
        }
        self.usb.count0 = 8;
        self.usb.csr0 |= 1;
        self.usb.intr_tx |= 1;
        self.usb.host = next;
    }
}

/// A MIDI message (whole, as a MIDI program sends it) as USB-MIDI event packets (cable 0).
pub fn packets(msg: &[u8]) -> Vec<u8> {
    let mut p = Vec::new();
    if msg.first() == Some(&0xf0) {
        let mut i = 0;
        while i < msg.len() {
            let k = (msg.len() - i).min(3);
            let end = i + k == msg.len();
            let cin = if !end { 4 } else { 4 + k as u8 };   // 4 continues; 5, 6, 7 end with 1, 2, 3 bytes
            p.push(cin);
            for j in 0..3 {
                p.push(if j < k { msg[i + j] } else { 0 });
            }
            i += k;
        }
    } else if let Some(&st) = msg.first() {
        if st >= 0x80 {
            let cin = if st >= 0xf0 { 0x0f } else { st >> 4 };
            p.extend_from_slice(&[cin, st, msg.get(1).copied().unwrap_or(0), msg.get(2).copied().unwrap_or(0)]);
        }
    }
    p
}

/// USB-MIDI event packets back into MIDI messages; `sx` holds a SysEx under way between calls.
pub fn messages(pk: &[u8], sx: &mut Vec<u8>) -> Vec<Vec<u8>> {
    let mut out = Vec::new();
    for c in pk.chunks_exact(4) {
        let (cin, d) = (c[0] & 15, &c[1..4]);
        match cin {
            4 => sx.extend_from_slice(d),
            5 | 6 | 7 => {
                sx.extend_from_slice(&d[..(cin - 4) as usize]);
                if sx.first() == Some(&0xf0) {
                    out.push(std::mem::take(sx));
                } else {
                    sx.clear();
                }
            }
            8..=0x0e => out.push(d[..if cin == 0x0c || cin == 0x0d { 2 } else { 3 }].to_vec()),
            0x0f => out.push(vec![d[0]]),
            _ => {}
        }
    }
    out
}
