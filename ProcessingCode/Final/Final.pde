import processing.serial.*;

float rotate=0;

SideView sw=new SideView();
UpView uw=new UpView();
float sideViewX=0;
float sideViewY=0;

Serial serial;

public void setup() {
  println(Serial.list());
  serial = new Serial(this, "/dev/tty.usbmodem141301", 9600);
  size(1000, 1000);
}
public void keyPressed() {
  switch(keyCode)
  {
  case UP:
    rotate+=1;
    break;
  case DOWN:
    rotate-=1;
  }
  if (rotate<-30)
    rotate=-30;
  if (rotate>30)
    rotate=30;
}

public void draw() {
  background(200);
  sw.draw();
  uw.draw();
  strokeWeight(4);
  stroke(0);
  line(width/2, 0, width/2, height);
  
  serial.write("go " + String.valueOf(sw.rot) + " " + String.valueOf(sw.x) + " " + String.valueOf(-sw.y) + "\n");
}
