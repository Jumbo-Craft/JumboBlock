import io.github.smile_ns.simplejson.SimpleJson;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) throws IOException{
        File[] images = new File("./images/").listFiles();
        SimpleJson output = new SimpleJson(new File("./output.json"));
        SimpleJson mat = new SimpleJson(new File("./material.json"));
        assert images != null;

        /*
        List<String> imgNames = new ArrayList<>();
        for (File img : images) {
            String filename = img.getName();
            String name = filename.substring(0, filename.lastIndexOf('.'));
            imgNames.add(name);
        }
         */
        List<String> matList = new ArrayList<>();
        mat.getList("material").forEach(e -> {
            matList.add(e.toString());
            /*
            String s = e.toString();
            if (!imgNames.contains(s)) System.out.println(s);
             */
        });

        for (File img : images) {
            String filename = img.getName();
            String name = filename.substring(0, filename.lastIndexOf('.'));
            if (!matList.contains(name)) continue;

            BufferedImage bi = ImageIO.read(img);
            int[] sum = new int[3];
            for (int i = 0;i < bi.getWidth();i++) {
                for (int j = 0;j < bi.getHeight();j++) {
                    int argb = bi.getRGB(i, j);
                    int[] rgb = {(argb >> 16) & 0xFF, (argb >> 8) & 0xFF, argb & 0xFF};
                    sum[0] += rgb[0];
                    sum[1] += rgb[1];
                    sum[2] += rgb[2];
                }
            }

            int size = bi.getHeight() * bi.getWidth();
            Color mono = new Color(sum[0] / size, sum[1] / size, sum[2] / size);
            System.out.println(name + ": " + mono.getRGB());
            output.put(name, mono.getRGB());
        }

        output.save();
    }
}
