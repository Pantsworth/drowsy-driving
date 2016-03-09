package com.example.yangbaiyu.drowsydriving2;

import android.content.Intent;
import android.os.Bundle;
import java.util.ArrayList;
import java.util.List;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.speech.RecognizerIntent;
import android.speech.tts.TextToSpeech;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import javax.net.ssl.HttpsURLConnection;
import android.app.Activity;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorManager;
import android.hardware.SensorEventListener;
import android.net.Uri;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import android.os.AsyncTask;
import android.util.Log;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.lang.InterruptedException;

import com.example.yangbaiyu.drowsydriving2.JsonParser;
//import com.google.android.gms.appindexing.Action;
//import com.google.android.gms.appindexing.AppIndex;
//import com.google.android.gms.common.api.GoogleApiClient;


import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class Main2Activity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener,SensorEventListener {
    // ListView listView;
    // ArrayAdapter<String> adapter;
    // String[] pi_data = {
    //        "Blink Rate:     ",  "Yawn Rate:     "
    //  };

    TextView yawnRate, blinkRate, blinkLength;
    String myBlinkRate, myYawnRate, myBlinkLength;
    private Sensor senAccelerometer;
    private SensorManager senSensorManager;
    private static int TTS_DATA_CHECK = 1;
    private static final int VOICE_RECOGNITION_REQUEST_CODE = 1234;
    private TextToSpeech tts = null;


    private boolean ttsIsInit = false;

    private long lastUpdate = 0;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.setDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);

        senSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        senAccelerometer = senSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        senSensorManager.registerListener(this, senAccelerometer, SensorManager.SENSOR_DELAY_NORMAL);

        //listView = (ListView) findViewById(R.id.listView);
        //adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1,pi_data);
        // listView.setAdapter(adapter);


        // Check to see if a recognition activity is present
        PackageManager pm = getPackageManager();
        List<ResolveInfo> activities = pm.queryIntentActivities(
                new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH), 0);

        findViews();
        new AsyncTaskParseJson().execute();


    }

    private void findViews() {
        blinkRate = (TextView) findViewById(R.id.main2_blinkRate);
        yawnRate = (TextView) findViewById(R.id.main2_yawnRate);
        blinkLength = (TextView) findViewById(R.id.main2_blinkLength);
    }

    public void writeSomething() {
        //TextView text = (TextView)findViewById(R.id.information);
        blinkRate.setText(myBlinkRate);
        yawnRate.setText(myYawnRate);
        blinkLength.setText(myBlinkLength);
    }


    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {
        Sensor mySensor = sensorEvent.sensor;

        if (mySensor.getType() == Sensor.TYPE_ACCELEROMETER) {

            long curTime = System.currentTimeMillis();

            if ((curTime - lastUpdate) > 2000) {
                lastUpdate = curTime;

                new AsyncTaskParseJson().execute();
                writeSomething();
            }
        }

    }

    protected void onResume() {
        super.onResume();
        senSensorManager.registerListener(this, senAccelerometer, SensorManager.SENSOR_DELAY_NORMAL);
    }

    protected void onPause() {
        super.onPause();
        senSensorManager.unregisterListener(this);
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }


    public class AsyncTaskParseJson extends AsyncTask<String, String, String> {

        final String TAG = "AsyncTaskParseJson.java";

        // set your json string url here
        String yourJsonStringUrl = "http://mhealthhelloworld-bpeynetti.c9users.io/getData.php";

        // contacts JSONArray
        JSONArray dataJsonArr = null;

        @Override
        protected void onPreExecute() {
        }

        @Override
        protected String doInBackground(String... arg0) {
//            AsyncTaskDone = false;
            try {

                // instantiate our json parser
                JsonParser jParser = new JsonParser();

                // get json string from url
                JSONObject json = jParser.getJSONFromUrl(yourJsonStringUrl);

                // get the array of users
                dataJsonArr = json.getJSONArray("Data");
                String yawnRate = "", blinkRate = "", blinkLength = "", threshold = "";

                // loop through all users
                for (int i = 0; i < 1; i++) {

                    JSONObject c = dataJsonArr.getJSONObject(i);

                    // Storing each json item in variable
                    yawnRate = c.getString("yawnRate");
                    blinkRate = c.getString("blinkRate");
                    blinkLength = c.getString("blinkLength");
                    threshold = c.getString("threshold");

                    int foo = Integer.parseInt(threshold);


                    if (foo >= 3) {//threshold
                        Intent intent = new Intent(TextToSpeech.Engine.ACTION_CHECK_TTS_DATA);
                        startActivityForResult(intent, TTS_DATA_CHECK);

                        try {
                            //通过Intent传递语音识别的模式，开启语音
                            Intent intent1 = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                            //语言模式和自由模式的语音识别
                            intent1.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
                            //提示语音开始
                            // intent1.putExtra(RecognizerIntent.EXTRA_PROMPT, "开始语音");  // not sure
                            //开始语音识别
                            startActivityForResult(intent1, VOICE_RECOGNITION_REQUEST_CODE );


                        } catch (Exception e) {
                            // TODO: handle exception
                            e.printStackTrace();
                            // Toast.makeText(getApplicationContext(), "找不到语音设备", 1).show();
                        }

                    }

                    // show the values in our logcat
                    Log.e(TAG, "yawnRate: " + yawnRate
                            + ", blinkRate: " + blinkRate
                            + ", blinkLength: " + blinkLength
                            + ", threshold: " + threshold);

                }
                //myText = ("Yawn:" + yawnRate + " , blink: " + blinkRate);
                myBlinkRate = ("" + blinkRate);
                myYawnRate = ("" + yawnRate);
                myBlinkLength = ("" + blinkLength);
                //writeSomething();
//                txtEdit.setText("Yawn:" + yawnRate + " , blink: "+blinkRate);


            } catch (JSONException e) {
                e.printStackTrace();
            }
//            AsyncTaskDone = true;
            return null;
        }
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {

            if (requestCode == TTS_DATA_CHECK && resultCode == TextToSpeech.Engine.CHECK_VOICE_DATA_PASS) {
                tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {

                    @Override
                    public void onInit(int status) {
                        if (status == TextToSpeech.SUCCESS) {
                            ttsIsInit = true;
                            if (tts.isLanguageAvailable(Locale.US) >= 0) {
                                tts.setPitch(1.1f);
                                tts.setSpeechRate(1.1f);
                                speak();
                            }
                        }
                    }

                    private void speak() {
                        if (tts != null && ttsIsInit) {
                            tts.speak("Hey Jimmy, do you want to go to Nabil's house?", TextToSpeech.QUEUE_FLUSH, null);


                        }

                    }
                });
            } else {
                Intent installAllVoice = new Intent(TextToSpeech.Engine.ACTION_INSTALL_TTS_DATA);
                startActivity(installAllVoice);
            }






        // voice recognition

            if ( requestCode ==  VOICE_RECOGNITION_REQUEST_CODE && resultCode == RESULT_OK) {
//                requestCode ==  VOICE_RECOGNITION_REQUEST_CODE &&
                // Fill the list view with the strings the recognizer thought it could have heard
                ArrayList<String> results = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);

                String resultString = "";
                for (int i = 0; i < results.size(); i++) {
                    resultString += results.get(i);
                }
                Log.d("Main2Activity", resultString);


//                System.out.println(resultString + "\n " +
//                            "\n" +
//                            "\n\n\n\n\n\n");
//
//                if (resultString.equals("YES")) { //
//                    //open googlemap

                    Intent intent = new Intent(android.content.Intent.ACTION_VIEW,
                            Uri.parse("http://maps.google.com/maps?saddr=20.344,34.34&daddr=20.5666,45.345"));
                    intent.setClassName("com.google.android.apps.maps", "com.google.android.maps.MapsActivity");
                    startActivity(intent);
//                }
            }

    }




    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main2, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.nav_camera) {
            // Handle the camera action
        } else if (id == R.id.nav_gallery) {

        } else if (id == R.id.nav_slideshow) {

        } else if (id == R.id.nav_manage) {

        } else if (id == R.id.nav_share) {

        } else if (id == R.id.nav_send) {

        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }
}









