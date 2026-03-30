package com.dad.parentingreminder

object ReminderData {

    fun getDailyReminders(): List<ReminderItem> = listOf(
        // Morning Routine
        ReminderItem(1,  "Good Morning Milk",       "Give baby their morning milk or formula (approx. 200ml)",       7,  0,  ReminderCategory.FEEDING),
        ReminderItem(2,  "Morning Wash",             "Wash baby's face, hands, and change into day clothes",          7, 30,  ReminderCategory.HYGIENE),
        ReminderItem(3,  "Breakfast",                "Soft foods: oatmeal, banana, scrambled eggs or toast",          8,  0,  ReminderCategory.FEEDING),
        ReminderItem(4,  "Daily Vitamins",           "Give vitamin D drops or multivitamin as prescribed",             8, 30,  ReminderCategory.HEALTH),

        // Morning Play
        ReminderItem(5,  "Morning Playtime",         "Free play with toys: blocks, stacking, push-pull toys",         9,  0,  ReminderCategory.PLAY),
        ReminderItem(6,  "Learning Activity",        "Naming objects, simple picture books, or music time",           9, 30,  ReminderCategory.DEVELOPMENT),
        ReminderItem(7,  "Morning Snack",            "Small snack: sliced fruit, crackers, or yogurt",               10, 30,  ReminderCategory.FEEDING),

        // First Nap
        ReminderItem(8,  "Morning Nap Time",         "1–1.5 hours nap. Ensure quiet, dim environment",               11,  0,  ReminderCategory.SLEEP),

        // Midday
        ReminderItem(9,  "Lunch",                    "Balanced meal: protein + veggies + carbs (soft & bite-sized)", 12, 30,  ReminderCategory.FEEDING),
        ReminderItem(10, "Post-Lunch Play",          "Gentle play or reading after lunch",                           13, 15,  ReminderCategory.PLAY),

        // Afternoon Nap
        ReminderItem(11, "Afternoon Nap",            "1.5–2 hour nap. Crucial for development and mood",             14,  0,  ReminderCategory.SLEEP),

        // Afternoon
        ReminderItem(12, "Afternoon Snack",          "Healthy snack: cheese cubes, veggie sticks, or fruit",         15, 30,  ReminderCategory.FEEDING),
        ReminderItem(13, "Outdoor Time",             "30–60 min outside: park, garden, or walk in stroller",         16,  0,  ReminderCategory.PLAY),
        ReminderItem(14, "Sensory Play",             "Sand, water play, playdough, or finger painting",              17,  0,  ReminderCategory.DEVELOPMENT),

        // Evening Routine
        ReminderItem(15, "Dinner",                   "Evening meal: soft cooked veggies, protein, rice or pasta",    18,  0,  ReminderCategory.FEEDING),
        ReminderItem(16, "Bath Time",                "Warm bath (not hot!). Good bonding time, 10–15 min",           18, 30,  ReminderCategory.HYGIENE),
        ReminderItem(17, "Teeth Brushing",           "Brush baby teeth gently with baby toothbrush & tiny toothpaste",19,  0,  ReminderCategory.HYGIENE),
        ReminderItem(18, "Storytime",                "Read 1–2 books together. Builds language and imagination",      19, 15,  ReminderCategory.DEVELOPMENT),
        ReminderItem(19, "Bedtime Milk",             "Final milk feed before sleep (approx. 150–200ml)",             19, 30,  ReminderCategory.FEEDING),
        ReminderItem(20, "Bedtime",                  "Put baby down to sleep. Consistent bedtime = better sleep",    20,  0,  ReminderCategory.SLEEP)
    )
}
