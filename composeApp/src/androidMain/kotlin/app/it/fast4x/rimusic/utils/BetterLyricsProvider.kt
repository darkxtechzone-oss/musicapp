package app.it.fast4x.rimusic.utils

/**
 * Stub replacement for the missing `:betterlyrics` module (assets/Better-Lyrics-main).
 *
 * The real "Better Lyrics" source module is not available in this build
 * (it was never present in the upstream repository this project was built
 * from). Rather than removing every UI reference to the "betterlyrics"
 * lyrics source scattered across Lyrics.kt, this stub keeps the same public
 * API and simply reports "no result found" every time it is called. The
 * existing fallback logic in Lyrics.kt will then automatically try the next
 * lyrics source (LRCLIB, Kugou, SimpMusic) instead.
 *
 * If the real Better Lyrics module source becomes available later, delete
 * this file and restore the real `assets/Better-Lyrics-main` module plus the
 * `implementation(projects.betterlyrics)` dependency line in
 * composeApp/build.gradle.kts.
 */
object BetterLyricsProvider {

    data class Result(
        val syncedLyrics: String? = null,
        val plainLyrics: String? = null
    )

    @Suppress("UNUSED_PARAMETER")
    suspend fun lyrics(
        title: String,
        artist: String,
        album: String?,
        durationSeconds: Int
    ): Result? = null
}
