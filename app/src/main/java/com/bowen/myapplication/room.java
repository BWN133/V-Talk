package com.bowen.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.animation.ObjectAnimator;
import android.os.Bundle;
import android.view.MotionEvent;
import android.widget.ImageView;

public class room extends AppCompatActivity {

    private ImageView imagePerson;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_room);

        imagePerson = findViewById(R.id.imagePerson);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        // Get the touch coordinates
        final float x = event.getX();
        final float y = event.getY() - imagePerson.getHeight();

        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:
                // Calculate the center position for the image
                float toX = x - (imagePerson.getWidth() / 2);
                float toY = y - (imagePerson.getHeight() / 2);

                // Animate X and Y properties
                ObjectAnimator animX = ObjectAnimator.ofFloat(imagePerson, "x", imagePerson.getX(), toX);
                ObjectAnimator animY = ObjectAnimator.ofFloat(imagePerson, "y", imagePerson.getY(), toY);

                animX.setDuration(500);
                animY.setDuration(500);

                animX.start();
                animY.start();
                break;
        }
        return true;
    }
}
