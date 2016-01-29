#include <iostream>
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "zmq.hpp"

using namespace std;
using namespace cv;

int main() {
    /***********************************
     *            CAMERA SETUP         *
     * *********************************/
    VideoCapture cap(0);
    if(!cap.isOpened()) return -1;
    cap.set(CAP_PROP_FRAME_WIDTH,160);
    cap.set(CAP_PROP_FRAME_HEIGHT,120);

    /***********************************
    *      COMMUNICATION SETUP         *
    * *********************************/
    zmq::context_t context (1);
    zmq::socket_t socket (context, ZMQ_REP);
    socket.bind ("tcp://*:5555");

    Mat img;
    for(;;) {
        zmq::message_t request;
        cap >> img;
//
//
        socket.recv (&request);
        cout << "Received Request" << endl;

        medianBlur(img, img, 3);
        Mat hsv_image;
        cvtColor(img, hsv_image, cv::COLOR_BGR2HSV);

        //red_filter
        Mat bright_red;
        Mat dark_red;
        inRange(hsv_image, cv::Scalar(160, 80, 70), cv::Scalar(180, 255, 255), bright_red);
        inRange(hsv_image, cv::Scalar(0, 100, 100), cv::Scalar(20, 255, 255), dark_red);
        Mat red_hue_image;
        addWeighted(bright_red, 1.0, dark_red, 1.0, 0.0, red_hue_image);
        GaussianBlur(red_hue_image, red_hue_image, cv::Size(9, 9), 2, 2);
//        imshow("frame", red_hue_image);
//        if(waitKey(30) >= 0) break;

//        //green_filter
//        Mat green_hue_image;
//        inRange(hsv_image, cv::Scalar(30, 90, 30), cv::Scalar(90, 230, 90), green_hue_image);
//        GaussianBlur(green_hue_image, green_hue_image, cv::Size(9, 9), 2, 2);

        //find contours from binary image
        int i;
        vector< vector<Point> > contours;
        findContours(red_hue_image, contours, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE); //find contours


        //find largest contour area
        vector<double> areas(contours.size());
        for(i = 0; i < contours.size(); i++) {
            areas[i] = contourArea(Mat(contours[i]));
        }

        //get index of largest contour
        double max;
        Point maxPosition;
        minMaxLoc(Mat(areas),0,&max,0,&maxPosition);

//          //draw largest contour.
//          drawContours(red_hue_image, contours, maxPosition.y, Scalar(255), CV_FILLED);

        Point center;
        Rect r;
        if (contours.size() >= 1) {
            r = boundingRect(contours[maxPosition.y]);
//                rectangle(red_hue_image, r.tl(),r.br(), CV_RGB(255, 0, 0), 3, 8, 0); //draw rectangle
        }
        //get centroid
        center.x = r.x + (r.width/2);
        center.y= r.y + (r.height/2);

        //  Send reply back to client
        string message;
        if (max > 300)
            message = to_string(max) + "," + to_string(center.x) + "," + to_string(center.y);
        else
            message = "None,0,0";

        zmq::message_t reply (message.length());
        memcpy ((void *) reply.data (), message.c_str(), message.length());
        socket.send (reply);
    }
}