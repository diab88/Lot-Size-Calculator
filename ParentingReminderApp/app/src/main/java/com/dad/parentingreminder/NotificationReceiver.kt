package com.dad.parentingreminder

import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import androidx.core.app.NotificationCompat

class NotificationReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        val reminderId = intent.getIntExtra("reminder_id", 0)
        val title = intent.getStringExtra("reminder_title") ?: "Baby Reminder"
        val description = intent.getStringExtra("reminder_description") ?: ""
        val category = intent.getStringExtra("reminder_category") ?: ""
        val emoji = intent.getStringExtra("reminder_emoji") ?: ""

        showNotification(context, reminderId, title, description, category, emoji)

        // Reschedule for tomorrow
        val reminders = ReminderData.getDailyReminders()
        val reminder = reminders.find { it.id == reminderId }
        reminder?.let { NotificationHelper.scheduleReminder(context, it) }
    }

    private fun showNotification(
        context: Context,
        id: Int,
        title: String,
        description: String,
        category: String,
        emoji: String
    ) {
        val tapIntent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        }
        val pendingIntent = PendingIntent.getActivity(
            context, id, tapIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(context, NotificationHelper.CHANNEL_ID)
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentTitle("$emoji $title")
            .setContentText(description)
            .setStyle(NotificationCompat.BigTextStyle().bigText(description))
            .setSubText(category)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .setVibrate(longArrayOf(0, 300, 200, 300))
            .build()

        val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.notify(id, notification)
    }
}
