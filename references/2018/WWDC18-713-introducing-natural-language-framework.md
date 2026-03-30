---
framework: Natural Language
title: "Introducing Natural Language Framework"
session: WWDC18-713
year: 2018
applies_to: iOS 12+
status: deprecated
superseded_by: null
shape: code-first
related: []
---

> **Deprecated:** This session covers the Natural Language framework as introduced in iOS 12. The framework itself remains available and largely unchanged; this reference covers the original APIs that replaced `NSLinguisticTagger`. For advanced on-device NLP, see Create ML text classifiers and the more recent `NLModel` APIs.

## Quick start

```swift
import NaturalLanguage

// Language detection
let recognizer = NLLanguageRecognizer()
recognizer.processString("Bonjour le monde")
let language = recognizer.dominantLanguage   // .french

// Tokenization
let tokenizer = NLTokenizer(unit: .word)
tokenizer.string = "Hello, world!"
tokenizer.enumerateTokens(in: tokenizer.string!.startIndex...) { range, _ in
    print(tokenizer.string![range])
    return true
}

// Named entity recognition
let tagger = NLTagger(tagSchemes: [.nameType])
tagger.string = "Tim Cook lives in Cupertino."
tagger.enumerateTags(in: tagger.string!.startIndex...,
                     unit: .word,
                     scheme: .nameType,
                     options: [.omitWhitespace, .omitPunctuation]) { tag, range in
    if let tag { print("\(tagger.string![range]): \(tag.rawValue)") }
    return true
}
```

## Key APIs

| Type | Role |
|---|---|
| `NLLanguageRecognizer` | Identifies language of a string; returns `NLLanguage` |
| `NLTokenizer` | Splits text into words, sentences, paragraphs, or documents |
| `NLTagger` | Applies tag schemes (POS, named entity, lemma, language) to tokens |
| `NLTagScheme` | Constants: `.tokenType`, `.lexicalClass`, `.nameType`, `.lemma`, `.language` |
| `NLLanguage` | Typed language constants replacing `NSLinguisticTag` strings |
| `NLModel` | Load a Core ML text classifier/word tagger for custom tagging (added later) |

## Common patterns

**Part-of-speech tagging**

```swift
let tagger = NLTagger(tagSchemes: [.lexicalClass])
tagger.string = "The quick brown fox jumps."
tagger.enumerateTags(in: tagger.string!.startIndex...,
                     unit: .word, scheme: .lexicalClass,
                     options: [.omitWhitespace, .omitPunctuation]) { tag, range in
    print("\(tagger.string![range]) — \(tag?.rawValue ?? "?")")
    return true
}
```

**Hypothesis language probabilities**

```swift
recognizer.processString(inputText)
let hypotheses = recognizer.languageHypotheses(withMaximum: 3)
// ["fr": 0.9, "it": 0.07, "pt": 0.03]
```

## Gotchas

- `NLTagger` is not thread-safe — create one per thread or use a serial queue.
- `enumerateTokens` requires the full string range; constructing ranges from substrings requires care with `String.Index`.
- Language detection accuracy improves with longer input; single-word detection is unreliable.
- `NSLinguisticTagger` still compiles on iOS 12+ but produces deprecation warnings — migrate to `NLTagger`.
