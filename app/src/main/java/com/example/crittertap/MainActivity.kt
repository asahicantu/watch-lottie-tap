package com.example.crittertap

import android.os.Bundle
import android.view.WindowManager
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.example.crittertap.ui.CritterApp
import com.example.crittertap.ui.theme.CritterTapTheme

/**
 * The entry point for the CritterTap application.
 *
 * This activity handles the window flags for keeping the screen on (essential for a toy)
 * and sets up the Compose theme and root application Composable.
 */
class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Tapping toys are no fun if the watch blanks after a few seconds.
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        setContent {
            CritterTapTheme {
                CritterApp()
            }
        }
    }
}
