package com.bowen.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.Toast;

public class questions extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_questions);

        SeekBar seekBarMood = findViewById(R.id.seekBar_mood);
        Button loginButton = findViewById(R.id.login_button);


//       TODO: use this info
        loginButton.setOnClickListener(view -> {

            int moodValue = seekBarMood.getProgress();


            Intent intent = new Intent(questions.this, room.class);


            intent.putExtra("moodValue", moodValue);

            startActivity(intent);
        });
    }
}
