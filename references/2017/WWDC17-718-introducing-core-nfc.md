---
framework: Core NFC
title: "Introducing Core NFC"
session: WWDC17-718
year: 2017
applies_to: iOS 11+
status: reference-only
superseded_by: null
shape: code-first
related: []
---

> **Reference-only (iOS 11+):** Core NFC introduced in iOS 11 remains the primary NFC API. iOS 13 expanded it with read/write support for multiple tag types (`NFCTagReaderSession`). The original NDEF reading API shown here is still valid.

## Quick start

```swift
import CoreNFC

class NFCReader: NSObject, NFCNDEFReaderSessionDelegate {
    var session: NFCNDEFReaderSession?

    func beginScan() {
        session = NFCNDEFReaderSession(delegate: self, queue: nil, invalidateAfterFirstRead: true)
        session?.alertMessage = "Hold your iPhone near an NFC tag."
        session?.begin()
    }

    func readerSession(_ session: NFCNDEFReaderSession,
                       didDetectNDEFs messages: [NFCNDEFMessage]) {
        for message in messages {
            for record in message.records {
                print(record.typeNameFormat, record.type, record.payload)
            }
        }
    }

    func readerSession(_ session: NFCNDEFReaderSession, didInvalidateWithError error: Error) {
        print(error.localizedDescription)
    }
}
```

## Key APIs

| Type | Role |
|---|---|
| `NFCNDEFReaderSession` | Scans for NDEF-formatted NFC tags (iOS 11+) |
| `NFCTagReaderSession` | Reads ISO 7816, ISO 15693, FeliCa, MIFARE tags (iOS 13+) |
| `NFCNDEFMessage` | Contains one or more `NFCNDEFPayload` records |
| `NFCNDEFPayload` | Single NDEF record: `typeNameFormat`, `type`, `identifier`, `payload` |

## Common patterns

**Parse a URI record**

```swift
func readerSession(_ session: NFCNDEFReaderSession,
                   didDetectNDEFs messages: [NFCNDEFMessage]) {
    for record in messages.first?.records ?? [] {
        if let url = record.wellKnownTypeURIPayload() {
            print("URL:", url)
        }
    }
}
```

## Gotchas

- NFC entitlement (`com.apple.developer.nfc.readersession.formats`) must be added to the app's entitlements file.
- Add `NFCReaderUsageDescription` to `Info.plist` (required since iOS 11).
- `NFCNDEFReaderSession` only reads NDEF tags. For raw tag access use `NFCTagReaderSession` (iOS 13+).
- NFC scanning is only available on iPhone 7 and later; always check `NFCNDEFReaderSession.readingAvailable` before presenting UI.
