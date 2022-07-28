public class UpView {
    float[] l = {0f, 16f, 15f, 10f};

    int diameter = 20;
    int lMic = diameter / 4;
    float scale = 15;

    public void draw() {
        pushMatrix();
        float shiftX = 3 * width / 4;
        float shiftY = height - lMic - diameter / 4;
         InversKinematics temp= new InversKinematics();
          double[] angles = temp.calc(rotate, (mouseX - sideViewX) / scale, (mouseY - sideViewY) / scale);
        translate(shiftX, shiftY);

//        System.out.println("rotate: " + angles[0]);
        rotate((float) angles[0]);
        float prevAngle = 0;
        float shadowLength = 0;
        for (int i = 0; i < angles.length; i++) {

            stroke(0);
            strokeWeight(1);
            fill(51, 204, 255);
            ellipse(0, 0, diameter + 5, diameter + 5);
            strokeWeight(20);
            stroke(51, 205, 255);
            prevAngle += angles[i];


            if (sin(prevAngle) != 0) shadowLength = l[i] * sin((float) prevAngle) * scale;
            line(0, 0, 0, -shadowLength);
            translate(0, -shadowLength);

        }
        noStroke();
        fill(56, 56, 201);
        stroke(56, 56, 201);
        line(0,0,0,-9*scale);
        popMatrix();


        //draw stick
        fill(102, 51, 0);
        noStroke();
        ellipse(shiftX,-27*scale+shiftY,20,20);
        ellipse(shiftX+10* scale,-27*scale+shiftY,20,20);
        ellipse(shiftX-10*scale,-27*scale+shiftY,20,20);
    }

}
