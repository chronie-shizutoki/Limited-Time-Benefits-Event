# Gift Activity Center

A multi-platform limited-time benefits event management system with Android client support.

## Project Overview

This project provides a comprehensive solution for managing and displaying limited-time promotional activities across multiple platforms. It consists of three main components:

- **Backend (Node.js)**: RESTful API server for data management and APK distribution
- **Android App**: Native Android application built with Jetpack Compose

## Features

### Backend API
- RESTful API endpoints for activities and markdown content
- APK file management and distribution
- Changelog management for version updates
- Static file serving
- CORS support for cross-origin requests

### Android Application
- Jetpack Compose UI with Miuix design system
- Three main screens: Home, Answers, Settings
- Automatic update checking and download
- Multi-language support
- Theme switching (Light/Dark/System)
- Markdown content rendering
- Responsive layout for different screen sizes

## Project Structure

```
gift/
├── android/              # Android application
│   ├── app/
│   │   └── src/
│   │       └── main/
│   │           ├── java/com/chronie/gift/
│   │           │   ├── data/           # Data managers
│   │           │   │   ├── DownloadManager.kt
│   │           │   │   ├── LanguageManager.kt
│   │           │   │   ├── ThemeManager.kt
│   │           │   │   └── UpdateChecker.kt
│   │           │   ├── ui/             # UI components
│   │           │   │   ├── components/
│   │           │   │   ├── markdown/
│   │           │   │   ├── navigation/
│   │           │   │   ├── screens/
│   │           │   │   └── theme/
│   │           │   ├── MainActivity.kt
│   │           │   └── GiftApplication.kt
│   │           └── res/                 # Resources
│   └── gradle/
├── server/              # Backend API
│   ├── data/            # Data files
│   └── main.js          # Server entry point
├── scripts/             # Utility scripts
├── package.json         # Node.js dependencies
└── start.bat           # Windows startup script
```

## Technology Stack

### Backend
- **Runtime**: Node.js
- **Framework**: Express.js
- **Dependencies**:
  - `cors` - Cross-origin resource sharing
  - `express` - Web framework
  - `http-proxy-middleware` - Proxy middleware
  - `node-fetch` - HTTP client

### Android Application
- **Language**: Kotlin
- **UI Framework**: Jetpack Compose
- **Design System**: Miuix KMP
- **Key Libraries**:
  - Ktor Client - HTTP client
  - Coil - Image loading
  - Kotlinx Serialization - JSON serialization
  - Miuix KMP - Design components
  - Navigation Compose - Navigation

## API Endpoints

### Activities
- `GET /api/activities` - Get list of activities

### APK Management
- `GET /api/download_apk` - Get list of available APKs
- `GET /api/download_apk/:filename` - Download specific APK file

### Markdown Content
- `GET /api/outdate-test/markdown` - Get list of markdown files
- `GET /api/outdate-test/markdown/:filename` - Get content of specific markdown file

## Installation

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn
- Android Studio (for Android development)
- JDK 11 or higher

### Backend Setup

1. Navigate to the project root directory
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the server:
   ```bash
   npm run dev
   ```
   Or on Windows:
   ```bash
   start.bat
   ```

The server will start on `http://localhost:3001` by default.

### Android App Setup

1. Open the `android` directory in Android Studio
2. Wait for Gradle sync to complete
3. Build and run the app on an emulator or physical device

### Data Configuration

Create the following data files in `server/data/`:

- `activities.json` - Activity list data
- `changelog.json` - Version changelog
- `outdate-test-markdown/` - Directory for markdown files

Example `activities.json`:
```json
{
  "activities": [
    {
      "title": "Activity Title",
      "url": "https://example.com"
    }
  ]
}
```

## Development

### Backend Development

The backend is a simple Express.js server. Key files:

- `server/main.js` - Main server file with API routes

### Android Development

The Android app follows modern Android development practices:

- Use Jetpack Compose for UI
- Follow MVVM architecture patterns
- Implement proper lifecycle management
- Use coroutines for asynchronous operations

## Multi-Language Support

The project supports four languages:
- English (en)
- Chinese Simplified (zh-CN)
- Chinese Traditional (zh-TW)
- Japanese (ja)

### Android App

Language strings are defined in `res/values/` directories:
- `values/` - Default (English)
- `values-zh-rCN/` - Chinese Simplified
- `values-zh-rTW/` - Chinese Traditional
- `values-ja/` - Japanese

## Version Management

### Android App Versioning

The Android app uses a timestamp-based versioning scheme:
- Format: `1.YYYYMMDD.HHMM`
- Example: `1.20260203.0031`

Version is automatically generated during build using system timestamp.

### Changelog

Changelogs are managed in `server/data/changelog.json` with support for multiple languages:

```json
{
  "changelog": {
    "en": "Version notes in English",
    "zh-cn": "Version notes in Chinese Simplified",
    "zh-tw": "Version notes in Chinese Traditional",
    "ja": "Version notes in Japanese"
  }
}
```

## Configuration

### Server Port

The server port can be configured via environment variable:
```bash
PORT=3001 npm start
```

### API Base URL

The Android app's API base URL is configured in `UpdateChecker.kt`. Update the `apiBaseUrl` variable to match your server address.

## Building

### Android APK

To build a release APK:

1. Open the project in Android Studio
2. Select Build > Generate Signed Bundle / APK
3. Follow the signing wizard
4. The APK will be generated in `app/release/`

Place the generated APK in `server/apk/` for distribution.

## License

NO LICENSE, DON'T USE THIS CODE FOR COMMERCIAL PURPOSES.

## Author

Chronie