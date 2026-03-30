package com.dad.parentingreminder

import android.content.Context
import android.graphics.Paint
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.CheckBox
import android.widget.TextView
import androidx.cardview.widget.CardView
import androidx.recyclerview.widget.RecyclerView

class ReminderAdapter(
    private val context: Context,
    private var reminders: List<ReminderItem>,
    private val onChecked: (ReminderItem, Boolean) -> Unit
) : RecyclerView.Adapter<ReminderAdapter.ViewHolder>() {

    private val categoryColors = mapOf(
        ReminderCategory.FEEDING     to 0xFFFF8F00.toInt(),  // amber
        ReminderCategory.SLEEP       to 0xFF5C6BC0.toInt(),  // indigo
        ReminderCategory.PLAY        to 0xFF43A047.toInt(),  // green
        ReminderCategory.HYGIENE     to 0xFF00ACC1.toInt(),  // cyan
        ReminderCategory.HEALTH      to 0xFFE53935.toInt(),  // red
        ReminderCategory.DEVELOPMENT to 0xFF8E24AA.toInt()   // purple
    )

    inner class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val card: CardView = itemView.findViewById(R.id.card_reminder)
        val tvEmoji: TextView = itemView.findViewById(R.id.tv_emoji)
        val tvTitle: TextView = itemView.findViewById(R.id.tv_title)
        val tvDescription: TextView = itemView.findViewById(R.id.tv_description)
        val tvTime: TextView = itemView.findViewById(R.id.tv_time)
        val tvCategory: TextView = itemView.findViewById(R.id.tv_category)
        val checkBox: CheckBox = itemView.findViewById(R.id.checkbox_done)
        val accentBar: View = itemView.findViewById(R.id.view_accent)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(context).inflate(R.layout.item_reminder, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val reminder = reminders[position]
        val color = categoryColors[reminder.category] ?: 0xFF607D8B.toInt()

        holder.tvEmoji.text = reminder.category.emoji
        holder.tvTitle.text = reminder.title
        holder.tvDescription.text = reminder.description
        holder.tvTime.text = reminder.timeLabel
        holder.tvCategory.text = reminder.category.displayName
        holder.accentBar.setBackgroundColor(color)
        holder.tvCategory.setTextColor(color)

        // Show done state
        holder.checkBox.setOnCheckedChangeListener(null)
        holder.checkBox.isChecked = reminder.isDone
        applyDoneStyle(holder, reminder.isDone)

        holder.checkBox.setOnCheckedChangeListener { _, isChecked ->
            reminder.isDone = isChecked
            applyDoneStyle(holder, isChecked)
            onChecked(reminder, isChecked)
        }
    }

    private fun applyDoneStyle(holder: ViewHolder, isDone: Boolean) {
        if (isDone) {
            holder.tvTitle.paintFlags = holder.tvTitle.paintFlags or Paint.STRIKE_THRU_TEXT_FLAG
            holder.tvTitle.alpha = 0.5f
            holder.tvDescription.alpha = 0.4f
            holder.tvTime.alpha = 0.4f
            holder.card.alpha = 0.75f
        } else {
            holder.tvTitle.paintFlags = holder.tvTitle.paintFlags and Paint.STRIKE_THRU_TEXT_FLAG.inv()
            holder.tvTitle.alpha = 1f
            holder.tvDescription.alpha = 1f
            holder.tvTime.alpha = 1f
            holder.card.alpha = 1f
        }
    }

    override fun getItemCount() = reminders.size

    fun updateList(newList: List<ReminderItem>) {
        reminders = newList
        notifyDataSetChanged()
    }
}
