package com.chronie.gift.ui.components

import androidx.compose.runtime.Composable
import androidx.compose.ui.res.stringResource
import com.chronie.gift.R
import top.yukonga.miuix.kmp.basic.FloatingNavigationBar
import top.yukonga.miuix.kmp.basic.FloatingNavigationBarMode
import top.yukonga.miuix.kmp.basic.NavigationItem
import top.yukonga.miuix.kmp.icon.MiuixIcons
import top.yukonga.miuix.kmp.icon.extended.HorizontalSplit
import top.yukonga.miuix.kmp.icon.extended.ListView
import top.yukonga.miuix.kmp.icon.extended.Settings
import top.yukonga.miuix.kmp.theme.MiuixTheme

@Composable
fun TabBar(
    selectedTab: String,
    onTabChange: (String) -> Unit
) {
    // Convert string tab to index
    val selectedIndex = when (selectedTab) {
        "home" -> 0
        "answers" -> 1
        "settings" -> 2
        else -> 0
    }

    // Define tab data using MiuixIcons
    val tabs = listOf(
        Triple("home", MiuixIcons.HorizontalSplit, stringResource(id = R.string.tab_home)),
        Triple("answers", MiuixIcons.ListView, stringResource(id = R.string.tab_answers)),
        Triple("settings", MiuixIcons.Settings, stringResource(id = R.string.tab_settings))
    )

    // Create NavigationItem list
    val navigationItems = tabs.map { NavigationItem(label = it.third, icon = it.second) }

    FloatingNavigationBar(
        items = navigationItems,
        selected = selectedIndex,
        onClick = { index -> onTabChange(tabs[index].first) },
        mode = FloatingNavigationBarMode.IconOnly,
        color = MiuixTheme.colorScheme.background.copy(alpha = 0.7f)
    )
}