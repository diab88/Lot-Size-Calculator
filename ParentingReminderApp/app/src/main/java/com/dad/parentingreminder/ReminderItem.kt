package com.dad.parentingreminder

enum class ReminderCategory(val displayName: String, val emoji: String) {
    FEEDING("Feeding", "🍼"),
    SLEEP("Sleep", "😴"),
    PLAY("Playtime", "🎮"),
    HYGIENE("Hygiene", "🛁"),
    HEALTH("Health", "💊"),
    DEVELOPMENT("Development", "📚")
}

data class ReminderItem(
    val id: Int,
    val title: String,
    val description: String,
    val timeHour: Int,
    val timeMinute: Int,
    val category: ReminderCategory,
    var isDone: Boolean = false
) {
    val timeLabel: String
        get() {
            val period = if (timeHour < 12) "AM" else "PM"
            val displayHour = when {
                timeHour == 0 -> 12
                timeHour > 12 -> timeHour - 12
                else -> timeHour
            }
            return "%d:%02d %s".format(displayHour, timeMinute, period)
        }
}
