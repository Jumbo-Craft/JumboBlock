import io.github.smile_ns.simplejson.SimpleJson;
import io.github.smile_ns.simplejson.SimpleJsonProperty;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.util.*;
import java.util.List;

public class Main {

    public static void main(String[] args) throws IOException {
        File[] files = new File("./input/jumbo_textures/").listFiles();
        assert files != null;
        recursive(files);
    }

    static void recursive(File[] files) throws IOException {
        for (File f : files) {
            if (Files.isDirectory(f.toPath())) {
                recursive(Objects.requireNonNull(f.listFiles()));
                continue;
            }

            /* ---recursive process here--- */
            //createJumboTexture(f);
            renderJumboTexture(new SimpleJson(f));
            //trim(f);
        }
    }

    static void createJumboTexture(File img) throws IOException {
        SimpleJson colorMap = new SimpleJson(new File("./input/color_map.json"));

        String filename = img.getName();
        String name = filename.substring(0, filename.lastIndexOf('.'));

        String dirPath = img.getPath().replace(".\\input\\textures\\", "").replace(filename, "");
        dirPath = "./output/jumbo_textures/" + dirPath.replace("\\", "/");
        new File(dirPath).mkdirs();

        SimpleJson jmbJson = new SimpleJson(new File(String.format("%s/%s.json", dirPath, name)));
        List<String> pixelList = new ArrayList<>();

        BufferedImage bi = ImageIO.read(img);
        for (int i = 0; i < bi.getWidth(); i++) {
            for (int j = 0; j < bi.getHeight(); j++) {
                String blockName = getClosestColorBlock(colorMap, bi.getRGB(i, j));
                pixelList.add(blockName);
            }
        }

        jmbJson.put("components", pixelList);
        jmbJson.save();
        System.out.println("saved: " + jmbJson.getFile().toPath());
    }

    static String getClosestColorBlock(SimpleJson colorMap, int argb) {
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

    static void renderJumboTexture(SimpleJson json) throws IOException {
        String filename = json.getFile().getName();
        String name = filename.substring(0, filename.lastIndexOf('.'));
        String dirPath = json.getFile().getPath().replace(".\\input\\jumbo_textures\\", "").replace(filename, "");
        dirPath = "./output/rendered_jumbo_block/" + dirPath.replace("\\", "/");
        new File(dirPath).mkdirs();

        File file = new File(String.format("%s/%s.mcfunction", dirPath, name));

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

        System.out.println("saved: " + file.getPath());
    }

    static void trim(File file) throws IOException {
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
