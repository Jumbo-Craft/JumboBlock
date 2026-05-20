import io.github.smile_ns.simplejson.SimpleJson;
import io.github.smile_ns.simplejson.SimpleJsonProperty;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;
import java.util.List;

public class Main {

    public static void main(String[] args) throws IOException {
        createJumboTexture();
        File[] files = new File("./jumbo_textures/").listFiles();
        assert files != null;
        for (File f : files) {
            //trim(f);
            String filename = f.getName();
            String name = filename.substring(0, filename.lastIndexOf('.'));
            SimpleJson json = new SimpleJson(new File("./jumbo_textures/" + name + ".json"));
            renderJumboTexture(json);
            System.out.println(name);
        }
    }

    public static void createJumboTexture() throws IOException {
        File[] images = new File("./textures/").listFiles();
        SimpleJson colorMap = new SimpleJson(new File("./color_map.json"));

        assert images != null;
        for (File img : images) {
            String filename = img.getName();
            String name = filename.substring(0, filename.lastIndexOf('.'));
            SimpleJson jmbJson = new SimpleJson(new File("./jumbo_textures/" + name + ".json"));
            List<String> pixelList = new ArrayList<>();
            //boolean replaced = false;

            BufferedImage bi = ImageIO.read(img);
            for (int i = 0; i < bi.getWidth(); i++) {
                for (int j = 0; j < bi.getHeight(); j++) {
                    String blockName = getClosestColorBlock(colorMap, bi.getRGB(i, j));
                    pixelList.add(blockName);
                    //replaced = replaced || blockName.equals("dead_brain_coral_block") || blockName.equals("dead_bubble_coral_block") || blockName.equals("dead_fire_coral_block") || blockName.equals("dead_horn_coral_block") || blockName.equals("dead_tube_coral_block");
                }
            }

            jmbJson.put("components", pixelList);
            jmbJson.save();
            //if (replaced) System.out.println(name + ": coral block!");
        }
    }

    public static String getClosestColorBlock(SimpleJson colorMap, int argb) {
        int a = (argb >> 24) & 0xFF;
        int r1 = (argb >> 16) & 0xFF;
        int g1 = (argb >> 8) & 0xFF;
        int b1 = argb & 0xFF;

        if (a < 255) return "structure_void";

        double minDis = 195075.0; // 255^2 * 3
        String closestBlock = "barrier";
        for (String k : colorMap.toMap().keySet()) {
            Color color = new Color(colorMap.getInt(k));
            int r2 = color.getRed();
            int g2 = color.getGreen();
            int b2 = color.getBlue();
            double dis = Math.pow(r2 - r1, 2) + Math.pow(g2 - g1, 2) + Math.pow(b2 - b1, 2);

            if (dis < minDis) {
                closestBlock = k;
                minDis = dis;
            }
        }

        return closestBlock;
    }

    public static void renderJumboTexture(SimpleJson json) throws IOException {
        String filename = json.getFile().getName();
        String name = filename.substring(0, filename.lastIndexOf('.'));
        File file = new File("./rendered_jumbo_block/" + name + ".mcfunction");
        List<Object> blockList = json.getList("components");
        FileWriter filewriter = new FileWriter(file);
        List<String> queue = new ArrayList<>();
        blockList.forEach(block -> {
            SimpleJson e = new SimpleJson();
            e.put("id", block.toString());
            queue.add(e.toString());
        });

        filewriter.write("$data modify storage builder direction set value $(direction)\n");
        String cmd = "data modify storage builder queue set value " + queue.toString();
        filewriter.write(cmd.replaceAll("\\r\\n|\\r|\\n", ""));
        filewriter.write("\nfunction builder:direction/direction_manager");
        filewriter.close();
    }

    public static void trim(File file) throws IOException {
        BufferedImage image = ImageIO.read(file);

        int w = image.getWidth();
        int h = image.getHeight();

        if (w > 16 || h > 16) {
            BufferedImage crop = image.getSubimage(0,0, 16, 16);
            ImageIO.write(crop, "PNG", file);

            String filename = file.getName();
            String name = filename.substring(0, filename.lastIndexOf('.'));
            System.out.println(name + ": " + w + "*" + h);
        }
    }
}
