---
framework: WeatherKit
title: "Meet WeatherKit"
session: WWDC22-10003
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: code-first
related: []
---

# Meet WeatherKit — WWDC22

WeatherKit provides Apple's weather data to apps, replacing the need for third-party weather APIs. It requires an Apple Developer entitlement and attribution in the UI.

## Core APIs

### WeatherService

```swift
import WeatherKit
import CoreLocation

let weatherService = WeatherService.shared

let location = CLLocation(latitude: 37.3861, longitude: -122.0839)
let weather = try await weatherService.weather(for: location)
```

### Current weather

```swift
let current = weather.currentWeather

let temp = current.temperature           // Measurement<UnitTemperature>
let condition = current.condition        // WeatherCondition enum
let feelsLike = current.apparentTemperature
let humidity = current.humidity          // Double (0.0–1.0)
let windSpeed = current.wind.speed       // Measurement<UnitSpeed>
let uvIndex = current.uvIndex            // UVIndex struct
let isDaylight = current.isDaylight      // Bool
```

### Hourly forecast

```swift
let hourly: Forecast<HourWeather> = weather.hourlyForecast

for hour in hourly.filter({ $0.date < Date().addingTimeInterval(86400) }) {
    print("\(hour.date): \(hour.temperature), \(hour.condition)")
}
```

### Daily forecast

```swift
let daily: Forecast<DayWeather> = weather.dailyForecast

for day in daily {
    print("\(day.date): High \(day.highTemperature), Low \(day.lowTemperature)")
    print("Precipitation chance: \(day.precipitationChance)")
}
```

### Minute-by-minute precipitation

```swift
// Available only in supported regions
if let minutely = weather.minuteForecast {
    for minute in minutely.prefix(60) {
        print("\(minute.date): \(minute.precipitationIntensity)")
    }
}
```

### Requesting specific datasets

```swift
// Only fetch what you need to reduce latency
let (current, daily) = try await weatherService.weather(
    for: location,
    including: .current, .daily
)
```

## Entitlement requirement

WeatherKit requires the **WeatherKit** capability in Xcode and an active App ID with WeatherKit enabled on the Apple Developer portal. Without the entitlement, all requests return an error.

## Attribution requirement

Apps using WeatherKit **must** display Apple Weather attribution:
```swift
// Use the provided link
Link("Weather data from Apple", destination: URL(string: "https://weatherkit.apple.com/legal-attribution.html")!)
```

## REST API

WeatherKit also exposes a REST API (for non-Apple platforms) using JWT authentication — see developer documentation for endpoint details.

## Compatibility notes

- Requires iOS 16+, macOS 13+, watchOS 9+, tvOS 16+
- Requires WeatherKit entitlement (free tier: 500k calls/month per app)
- `CLLocation` (CoreLocation) is required to specify coordinates
- All `WeatherService` calls are `async throws`
