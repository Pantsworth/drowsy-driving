package com.example.yangbaiyu.drowsydriving2;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import org.w3c.dom.Text;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void onClick_login(View v) {
        Intent intent_login = new Intent("com.example.yangbaiyu.drowsydriving2.LoginActivity2");
        startActivity(intent_login);

    }
    public void onClick_nav(View v) {
        Intent intent_nav = new Intent("com.example.yangbaiyu.drowsydriving2.Main2Activity");
        startActivity(intent_nav);
    }


}

