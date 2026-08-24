package com.example.crittertap

import android.os.Bundle
import android.view.WindowManager
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.example.crittertap.ui.CritterApp
import com.example.crittertap.ui.theme.CritterTapTheme

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
