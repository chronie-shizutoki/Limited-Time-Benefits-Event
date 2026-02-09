package com.chronie.gift.ui.theme

import androidx.compose.runtime.Stable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import java.util.Locale

@Stable
class LanguageController(
    initialLanguageCode: String = "en",
) {
    var languageCode: String by mutableStateOf(initialLanguageCode)

    val currentLocale: Locale
        get() = when (languageCode) {
            "en" -> Locale.ENGLISH
            "ja" -> Locale.JAPANESE
            "zh-CN" -> Locale.SIMPLIFIED_CHINESE
            "zh-TW" -> Locale.TRADITIONAL_CHINESE
            else -> Locale.ENGLISH
        }
}
