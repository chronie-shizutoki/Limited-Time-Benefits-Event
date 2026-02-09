package com.chronie.gift.data

import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.os.Build
import android.os.LocaleList
import android.content.SharedPreferences
import java.util.Locale

class LanguageManager(private val context: Context) {
    companion object {
        private const val LANGUAGE_KEY = "preferred_language"
        private const val DEFAULT_LANGUAGE = "en"
        private const val PREF_NAME = "app_preferences"
    }

    // Get SharedPreferences instance
    private fun getPreferences(): SharedPreferences {
        return context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)
    }

    // Save language setting
    fun saveLanguage(languageCode: String) {
        val preferences = getPreferences()
        preferences.edit().putString(LANGUAGE_KEY, languageCode).apply()
    }

    // Get saved language setting
    fun getSavedLanguage(): String {
        val preferences = getPreferences()
        return preferences.getString(LANGUAGE_KEY, DEFAULT_LANGUAGE) ?: DEFAULT_LANGUAGE
    }

    // Apply language setting
    fun applyLanguage(languageCode: String) {
        val locale = when (languageCode) {
            "zh-CN" -> Locale.SIMPLIFIED_CHINESE
            "zh-TW" -> Locale.TRADITIONAL_CHINESE
            "en" -> Locale.ENGLISH
            "ja" -> Locale.JAPANESE
            else -> Locale.SIMPLIFIED_CHINESE
        }

        Locale.setDefault(locale)

        // Update current context configuration
        val resources = context.resources
        val configuration = Configuration(resources.configuration)
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR1) {
            configuration.setLocale(locale)
        } else {
            @Suppress("DEPRECATION")
            configuration.locale = locale
        }
        
        // Update resources configuration
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            val localeList = LocaleList(locale)
            configuration.setLocales(localeList)
        } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR1) {
            configuration.setLocale(locale)
        } else {
            @Suppress("DEPRECATION")
            configuration.locale = locale
        }
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR1) {
            context.createConfigurationContext(configuration)
        } else {
            @Suppress("DEPRECATION")
            resources.updateConfiguration(configuration, resources.displayMetrics)
        }
        
        // Update application context configuration
        val appContext = context.applicationContext
        val appConfig = Configuration(appContext.resources.configuration)
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            val localeList = LocaleList(locale)
            appConfig.setLocales(localeList)
        } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR1) {
            appConfig.setLocale(locale)
        } else {
            @Suppress("DEPRECATION")
            appConfig.locale = locale
        }
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR1) {
            appContext.createConfigurationContext(appConfig)
        } else {
            @Suppress("DEPRECATION")
            appContext.resources.updateConfiguration(appConfig, appContext.resources.displayMetrics)
        }
    }

    // Get current resources language setting
    fun getCurrentLanguage(): String {
        val resources = context.resources
        val configuration = resources.configuration
        val locale = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            configuration.locales[0]
        } else {
            @Suppress("DEPRECATION")
            configuration.locale
        }

        return when (locale.language) {
            "zh" -> if (locale.country == "TW" || locale.country == "HK" || locale.country == "MO") {
                "zh-TW"
            } else {
                "zh-CN"
            }
            "en" -> "en"
            "ja" -> "ja"
            else -> DEFAULT_LANGUAGE
        }
    }
}