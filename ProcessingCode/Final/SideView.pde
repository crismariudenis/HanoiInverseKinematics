public class SideView {
    float[] l = {0f, 16f, 15f, 10f};

    int diameter = 20;
    int lMic = diameter / 4;
    float scale = 15;
    float rot, x, y;


    SideView() {
     
      
    }

    public void draw() {
        part1Draw();
//        p.ellipse();
    }

    public void part1Draw() {
        pushMatrix();
        sideViewX = diameter;
        sideViewY = height - lMic - 200;
        InversKinematics temp= new InversKinematics();
        double[] angles = temp.calc(rotate, (mouseX - sideViewX) / scale, (mouseY - sideViewY) / scale);
        rot = rotate;
        x = (mouseX - sideViewX) / scale;
        y = (mouseY - sideViewY) / scale;
        translate(sideViewX, sideViewY);

//        System.out.println(p.mouseX/scale+" "+p.mouseY/scale);
        float prevAngle = 0;
        for (int i = 0; i < angles.length; i++) {
            stroke(0);
            strokeWeight(1);
            fill(51, 204, 255);
            ellipse(0, 0, diameter + 5, diameter + 5);
            strokeWeight(20);
            stroke(51, 205, 255);
            prevAngle += angles[i];
            line(0, 0, sin(prevAngle) * l[i] * scale, -cos(prevAngle) * l[i] * scale);
            translate(sin(prevAngle) * l[i] * scale, -cos(prevAngle) * l[i] * scale);
        }
        System.out.println();
        noStroke();
        fill(56, 56, 201);
        rect(0, 0, 9f * scale, scale);


        ///stalp

        popMatrix();
        fill(102, 51, 0);
        rect(27 * scale + sideViewX, sideViewY, 10, 50);

    }


}

