public class InversKinematics {
    final static double l1 = 2.5d;
    final static double l2 = 16d;
    final static double l3 = 15d;

   public double[] calc(double x, double y, double z) {

        try {
            double q0 = Math.atan(x / y);
            //a1 -> l3
            //a2 -> l2
            //q1 -> q3
            x = Math.sqrt(x * x + y * y);
            y = z;
            double a1 = l3;
            double a2 = l2;
            double q2 = Math.acos(((x * x + y * y - a1 * a1 - a2 * a2) / (2 * a1 * a2)));
            double q1 = Math.atan(y / x) - Math.atan((a2 * Math.sin(q2)) / (a1 + a2 * Math.cos(q2)));

            q1+=90;
            if(q1<0)
                q1+=PI;
//            return new double[]{10,20,30,40};
            return new double[]{-q0, q1, q2};
        } catch (Exception e) {
            System.out.println("Error coleg");
            return new double[]{};
        }
    }

}
