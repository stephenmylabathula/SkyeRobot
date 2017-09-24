package com.stephenmylabathula.blue.skye;

import android.support.v7.app.AppCompatActivity;
import android.os.*;
import android.view.MotionEvent;
import android.view.View;
import android.widget.*;
import android.net.*;
import com.jcraft.jsch.*;
import java.util.*;
import java.io.*;
import java.net.*;

public class ControlActivity extends AppCompatActivity {

    @Override
    protected void onDestroy(){
        new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/CleanUp.py");
        super.onDestroy();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_control);
        VideoView mVideoView = (VideoView) findViewById(R.id.videoView);
        MediaController mediaController = new MediaController(this);
        new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/InitializeController.py");
        mVideoView.setMediaController(mediaController);
        mVideoView.setVideoURI(Uri.parse("http://10.126.40.22:8090"));
        mVideoView.start();

        //Init Gui Handlers
        Button turnHeadLeft = (Button) findViewById(R.id.btnLeftHead);
        Button turnHeadRight = (Button) findViewById(R.id.btnRightHead);
        Button turnHeadCenter = (Button) findViewById(R.id.btnCenterHead);
        Button flipWingUp = (Button) findViewById(R.id.btnWingUp);
        Button flipWingMid = (Button) findViewById(R.id.btnWingMid);
        Button flipWingDown = (Button) findViewById(R.id.btnWingDown);
        Button goForward = (Button) findViewById(R.id.btnForward);
        Button goReverse = (Button) findViewById(R.id.btnReverse);
        Button goLeft = (Button) findViewById(R.id.btnLeft);
        Button goRight = (Button) findViewById(R.id.btnRight);
        Button driftLeft = (Button) findViewById(R.id.btnDriftLeft);
        Button driftRight = (Button) findViewById(R.id.btnDriftRight);

        turnHeadLeft.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/HeadLeft.py");
            }
        });

        turnHeadRight.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/HeadRight.py");
            }
        });

        turnHeadCenter.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/HeadCenter.py");
            }
        });

        flipWingUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/LeftWingUp.py");
            }
        });

        flipWingMid.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/LeftWingMid.py");
            }
        });

        flipWingDown.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/LeftWingDown.py");
            }
        });

        goForward.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                if (motionEvent.getAction() == MotionEvent.ACTION_DOWN){
                    new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/ForwardFast.py");
                }
                else if (motionEvent.getAction() == MotionEvent.ACTION_UP){
                    new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/StopMotors.py");
                }
                return true;
            }
        });

        goReverse.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                if (motionEvent.getAction() == MotionEvent.ACTION_DOWN){
                    new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/ReverseFast.py");
                }
                else if (motionEvent.getAction() == MotionEvent.ACTION_UP){
                    new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/StopMotors.py");
                }
                return true;
            }
        });

        goLeft.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                if (motionEvent.getAction() == MotionEvent.ACTION_DOWN){
                    new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/LeftFast.py");
                }
                else if (motionEvent.getAction() == MotionEvent.ACTION_UP){
                    new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/StopMotors.py");
                }
                return true;
            }
        });

        goRight.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                if (motionEvent.getAction() == MotionEvent.ACTION_DOWN){
                    new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/RightFast.py");
                }
                else if (motionEvent.getAction() == MotionEvent.ACTION_UP){
                    new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/StopMotors.py");
                }
                return true;
            }
        });

        driftLeft.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                if (motionEvent.getAction() == MotionEvent.ACTION_DOWN){
                    new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/LeftDriftFast.py");
                }
                else if (motionEvent.getAction() == MotionEvent.ACTION_UP){
                    new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/StopMotors.py");
                }
                return true;
            }
        });

        driftRight.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                if (motionEvent.getAction() == MotionEvent.ACTION_DOWN){
                    new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/RightDriftFast.py");
                }
                else if (motionEvent.getAction() == MotionEvent.ACTION_UP){
                    new LongOperation().execute("python3 ~/Documents/SkyeRobot/SkyeMotionControl/StopMotors.py");
                }
                return true;
            }
        });

    }

    private class LongOperation extends AsyncTask<String, Void, String> {

        @Override
        protected String doInBackground(String... params) {
            try {
                JSch jsch = new JSch();
                Session session = jsch.getSession("pi", "10.126.40.22", 22);
                session.setPassword("raspberry");
                Properties config = new Properties();
                config.put("StrictHostKeyChecking", "no");
                session.setConfig(config);
                session.connect();

                ChannelExec channel = (ChannelExec) session.openChannel("exec");
                BufferedReader in = new BufferedReader(new InputStreamReader(channel.getInputStream()));
                channel.setCommand(params[0]);
                channel.connect();

                String msg = null;
                while ((msg = in.readLine()) != null) {
                    System.out.println(msg);
                }

                channel.disconnect();
                session.disconnect();
            } catch (Exception e) {
                e.printStackTrace();
            }
            return "Executed";
        }

        @Override
        protected void onPostExecute(String result) {
        }

        @Override
        protected void onPreExecute() {}

        @Override
        protected void onProgressUpdate(Void... values) {}
    }
}



