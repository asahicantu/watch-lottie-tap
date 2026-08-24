# Lottie keeps its own rules; nothing extra needed for this app.

# okio (pulled in by Lottie for loading animations over the network) references
# JSR-305 annotations that are not on the Android classpath.
-dontwarn javax.annotation.**
