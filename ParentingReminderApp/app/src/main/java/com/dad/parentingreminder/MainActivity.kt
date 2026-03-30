package com.dad.parentingreminder

import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.widget.TextView
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.chip.Chip
import com.google.android.material.chip.ChipGroup
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.google.android.material.snackbar.Snackbar
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class MainActivity : AppCompatActivity() {

    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: ReminderAdapter
    private lateinit var chipGroup: ChipGroup
    private lateinit var tvDate: TextView
    private lateinit var tvProgress: TextView
    private lateinit var fab: FloatingActionButton

    private var allReminders = ReminderData.getDailyReminders().toMutableList()
    private var selectedCategory: ReminderCategory? = null

    companion object {
        private const val NOTIF_PERMISSION_CODE = 100
        private const val PREFS_NAME = "reminder_prefs"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        setSupportActionBar(findViewById(R.id.toolbar))
        supportActionBar?.title = ""

        tvDate = findViewById(R.id.tv_date)
        tvProgress = findViewById(R.id.tv_progress)
        chipGroup = findViewById(R.id.chip_group_filter)
        recyclerView = findViewById(R.id.recycler_reminders)
        fab = findViewById(R.id.fab_reset)

        // Set current date
        val dateFormat = SimpleDateFormat("EEEE, MMMM d", Locale.getDefault())
        tvDate.text = dateFormat.format(Date())

        // Restore saved done states
        restoreDoneStates()

        // Setup RecyclerView
        adapter = ReminderAdapter(this, getFilteredReminders()) { reminder, isDone ->
            saveDoneState(reminder.id, isDone)
            updateProgress()
        }
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = adapter

        // Setup category filter chips
        setupChips()
        updateProgress()

        // Setup FAB to reset daily tasks
        fab.setOnClickListener {
            showResetConfirmation()
        }

        // Request notification permission (Android 13+)
        NotificationHelper.createNotificationChannel(this)
        requestNotificationPermission()
    }

    private fun setupChips() {
        val allChip = chipGroup.getChildAt(0) as Chip
        allChip.isChecked = true
        allChip.setOnCheckedChangeListener { _, checked ->
            if (checked) {
                selectedCategory = null
                adapter.updateList(getFilteredReminders())
            }
        }

        ReminderCategory.values().forEachIndexed { index, category ->
            val chip = chipGroup.getChildAt(index + 1) as? Chip ?: return@forEachIndexed
            chip.text = "${category.emoji} ${category.displayName}"
            chip.setOnCheckedChangeListener { _, checked ->
                if (checked) {
                    selectedCategory = category
                    adapter.updateList(getFilteredReminders())
                }
            }
        }
    }

    private fun getFilteredReminders(): List<ReminderItem> {
        return if (selectedCategory == null) allReminders
        else allReminders.filter { it.category == selectedCategory }
    }

    private fun updateProgress() {
        val done = allReminders.count { it.isDone }
        val total = allReminders.size
        tvProgress.text = "Today: $done / $total tasks done"
    }

    private fun saveDoneState(id: Int, done: Boolean) {
        val prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
        val today = SimpleDateFormat("yyyyMMdd", Locale.getDefault()).format(Date())
        prefs.edit().putBoolean("${today}_$id", done).apply()
    }

    private fun restoreDoneStates() {
        val prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
        val today = SimpleDateFormat("yyyyMMdd", Locale.getDefault()).format(Date())
        allReminders.forEach { reminder ->
            reminder.isDone = prefs.getBoolean("${today}_${reminder.id}", false)
        }
    }

    private fun showResetConfirmation() {
        AlertDialog.Builder(this)
            .setTitle("Reset Today's Tasks")
            .setMessage("Mark all tasks as not done for a fresh start?")
            .setPositiveButton("Reset") { _, _ ->
                val today = SimpleDateFormat("yyyyMMdd", Locale.getDefault()).format(Date())
                val prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
                val editor = prefs.edit()
                allReminders.forEach { reminder ->
                    reminder.isDone = false
                    editor.remove("${today}_${reminder.id}")
                }
                editor.apply()
                adapter.updateList(getFilteredReminders())
                updateProgress()
                Snackbar.make(recyclerView, "Tasks reset for today!", Snackbar.LENGTH_SHORT).show()
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun requestNotificationPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)
                != PackageManager.PERMISSION_GRANTED
            ) {
                ActivityCompat.requestPermissions(
                    this,
                    arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                    NOTIF_PERMISSION_CODE
                )
            } else {
                NotificationHelper.scheduleAllReminders(this)
            }
        } else {
            NotificationHelper.scheduleAllReminders(this)
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int, permissions: Array<out String>, grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == NOTIF_PERMISSION_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                NotificationHelper.scheduleAllReminders(this)
                Snackbar.make(recyclerView, "Notifications enabled!", Snackbar.LENGTH_SHORT).show()
            }
        }
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.main_menu, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_info -> {
                showInfoDialog()
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    private fun showInfoDialog() {
        AlertDialog.Builder(this)
            .setTitle("Dad's Little Helper")
            .setMessage(
                "This app reminds you of your daily duties as a caring father for your 1.5-year-old.\n\n" +
                "• All reminders repeat every day\n" +
                "• Tap the checkbox to mark a task done\n" +
                "• Tasks reset automatically each day\n" +
                "• Use the filter chips to view by category\n\n" +
                "You're doing great, Dad! \uD83D\uDC76"
            )
            .setPositiveButton("Got it!", null)
            .show()
    }
}
