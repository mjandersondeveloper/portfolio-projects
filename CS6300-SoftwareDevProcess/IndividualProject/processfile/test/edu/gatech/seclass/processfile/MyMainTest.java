package edu.gatech.seclass.processfile;

import org.junit.After;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TemporaryFolder;

import java.io.*;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class MyMainTest {
    private ByteArrayOutputStream outStream;
    private ByteArrayOutputStream errStream;
    private PrintStream outOrig;
    private PrintStream errOrig;
    private final Charset charset = StandardCharsets.UTF_8;

    @Rule
    public TemporaryFolder temporaryFolder = new TemporaryFolder();

    @Before
    public void setUp() throws Exception {
        outStream = new ByteArrayOutputStream();
        PrintStream out = new PrintStream(outStream);
        errStream = new ByteArrayOutputStream();
        PrintStream err = new PrintStream(errStream);
        outOrig = System.out;
        errOrig = System.err;
        System.setOut(out);
        System.setErr(err);
    }

    @After
    public void tearDown() throws Exception {
        System.setOut(outOrig);
        System.setErr(errOrig);
    }

    /*
     *  TEST UTILITIES
     */

    // Create File Utility
    private File createTmpFile() throws Exception {
        File tmpfile = temporaryFolder.newFile();
        tmpfile.deleteOnExit();
        return tmpfile;
    }

    // Write File Utility
    private File createInputFile(String input) throws Exception {
        File file =  createTmpFile();

        OutputStreamWriter fileWriter =
                new OutputStreamWriter(new FileOutputStream(file), StandardCharsets.UTF_8);

        fileWriter.write(input);

        fileWriter.close();
        return file;
    }

    private String getFileContent(String filename) {
        String content = null;
        try {
            content = new String(Files.readAllBytes(Paths.get(filename)), charset);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return content;
    }

    /*
     *  TEST FRAMES
     */

    // Frame #1: <Test  1 in file catpart.txt.tsl>
    @Test
    public void processfileTest1() {
        String[] args = {"-s", "test", "-f"};
        Main.main(args);
        assertEquals("Usage: processfile [ -f | -n | -s string | -r string1 string2 | -g | -i | -p  ] FILE", errStream.toString().trim());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
    }

    // Frame #2: <Test  2 in file catpart.txt.tsl>
    @Test
    public void processfileTest2() throws Exception {
        String input = "Hey mom!";
        File inputFile = createInputFile(input);
        String[] args = {"-s", inputFile.getPath()};
        Main.main(args);
        assertEquals("Usage: processfile [ -f | -n | -s string | -r string1 string2 | -g | -i | -p  ] FILE", errStream.toString().trim());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
    }

    // Frame 3: <Test  3 in file catpart.txt.tsl>
    @Test
    public void processfileTest3() throws Exception {
        String input = "Hey dad!";
        File inputFile = createInputFile(input);
        String[] args = {"-r", "", inputFile.getPath()};
        Main.main(args);
        assertEquals("Usage: processfile [ -f | -n | -s string | -r string1 string2 | -g | -i | -p  ] FILE", errStream.toString().trim());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
    }

    // Frame #4: <Test  4 in file catpart.txt.tsl>
    @Test
    public void processfileTest4() throws Exception {
        String input = "This is invalid.";
        File inputFile = createInputFile(input);
        String[] args = {"-g", inputFile.getPath()};
        Main.main(args);
        assertEquals("Usage: processfile [ -f | -n | -s string | -r string1 string2 | -g | -i | -p  ] FILE", errStream.toString().trim());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
    }

    // Frame #5: <Test  5 in file catpart.txt.tsl>
    @Test
    public void processfileTest5() throws Exception {
        String input = "This is also invalid.";
        File inputFile = createInputFile(input);
        String[] args = {"-i", inputFile.getPath()};
        Main.main(args);
        assertEquals("Usage: processfile [ -f | -n | -s string | -r string1 string2 | -g | -i | -p  ] FILE", errStream.toString().trim());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
    }

    // Frame #6: <Test  6 in file catpart.txt.tsl>
    @Test
    public void processfileTest6() throws Exception {
        String input = "This prefix is missing an input!";
        File inputFile = createInputFile(input);
        String[] args = {"-p", inputFile.getPath()};
        Main.main(args);
        assertEquals("Usage: processfile [ -f | -n | -s string | -r string1 string2 | -g | -i | -p  ] FILE", errStream.toString().trim());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
    }

    // Frame #7: <Test  7 in file catpart.txt.tsl>
    @Test
    public void processfileTest7() throws Exception {
        String input = "Buzz The Mascot";

        File inputFile = createInputFile(input);
        String[] args = {inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", input, outStream.toString());
        assertEquals("Input not file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #8: <Test  8 in file catpart.txt.tsl>
    @Test
    public void processfileTest8() throws Exception {
        String input = "I have a cow. Can I have a chicken?";
        String expected = "I have a cow. Can I have a dog?";

        File inputFile = createInputFile(input);
        String[] args = {"-r", "cow", "dog", "-r", "chicken", "dog", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", expected, getFileContent(inputFile.getPath()));
    }

    // Frame #9: <Test  9 in file catpart.txt.tsl>
    @Test
    public void processfileTest9() throws Exception {
        String input = "I lik3 noodles" + System.lineSeparator()
                + "Do you also like noodles?" + System.lineSeparator()
                + "Noodles are like great!" + System.lineSeparator();
        String expected = "I love noodles" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-s", "3", "-r", "lik3", "love", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input not file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #10: <Test  10 in file catpart.txt.tsl>
    @Test
    public void processfileTest10() throws Exception {
        String input = "I lik3 noodles" + System.lineSeparator()
                + "Do you also like noodles?" + System.lineSeparator()
                + "Noodles are like great!" + System.lineSeparator();
        String expected = "#I love noodles" + System.lineSeparator()
                + "#Do you also like noodles?" + System.lineSeparator()
                + "#Noodles are like great!" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-p", "#", "-r", "lik3", "love", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input not file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #11: <Test  11 in file catpart.txt.tsl>
    @Test
    public void processfileTest11() throws Exception {
        String input = "I lik3 noodles" + System.lineSeparator()
                + "you also like noodles?" + System.lineSeparator()
                + "the noodles be like great!" + System.lineSeparator();
        String expected = "*I lik3 noodles" + System.lineSeparator()
                + "*you also hate noodles?" + System.lineSeparator()
                + "*the noodles be hate great!" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-s", "ood", "-p", "*", "-r", "like", "hate", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input not file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #12: <Test  12 in file catpart.txt.tsl>
    @Test
    public void processfileTest12() throws Exception {
        String input = "First Line" + System.lineSeparator()
                + "Second line" + System.lineSeparator()
                + "Third linE" + System.lineSeparator();
        String expected = "1 First Line" + System.lineSeparator()
                + "2 Second line" + System.lineSeparator()
                + "3 Third linE" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-s", "", "-n", "-i", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", expected, getFileContent(inputFile.getPath()));
    }

    // Frame #13: <Test  13 in file catpart.txt.tsl>
    @Test
    public void processfileTest13() throws Exception {
        String input = "First line" + System.lineSeparator()
                + "Second line" + System.lineSeparator()
                + "Third line" + System.lineSeparator();
        String expected = "1 First line" + System.lineSeparator()
                + "2 Second line" + System.lineSeparator()
                + "3 Third line" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-s", "", "-n", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", expected, getFileContent(inputFile.getPath()));
    }

    // Frame #14: <Test  14 in file catpart.txt.tsl>
    @Test
    public void processfileTest14() throws Exception {
        String input = "TEST ONE" + System.lineSeparator()
                + "test two" + System.lineSeparator()
                + "test Three" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-s", "", "-i", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #15: <Test  15 in file catpart.txt.tsl>
    @Test
    public void processfileTest15() throws Exception {
        String input = "This should be returned" + System.lineSeparator()
                + "And this" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-s", "", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #16: <Test  16 in file catpart.txt.tsl>
    @Test
    public void processfileTest16() throws Exception {
        String input = "File is not edited" + System.lineSeparator()
                + "Because stdout is" + System.lineSeparator();

        String expected = "1 File is not edited" + System.lineSeparator()
                + "2 Because stdout is" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-s", "", "-n", "-i", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input file not modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #17: <Test  17 in file catpart.txt.tsl>
    @Test
    public void processfileTest17() throws Exception {
        String input = "File is not edited" + System.lineSeparator()
                + "Because stdout is" + System.lineSeparator();

        String expected = "1 File is not edited" + System.lineSeparator()
                + "2 Because stdout is" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-s", "", "-n", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input file not modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #18: <Test  18 in file catpart.txt.tsl>
    @Test
    public void processfileTest18() throws Exception {
        String input = "File is not EditeD" + System.lineSeparator()
                + "Because Stdout iS" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-s", "", "-i", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", input, outStream.toString());
        assertEquals("Input file not modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #19: <Test  19 in file catpart.txt.tsl>
    @Test
    public void processfileTest19() throws Exception {
        String input = "Fil3 is not edit3d" + System.lineSeparator()
                + "Because stdout is" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-s", "", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", input, outStream.toString());
        assertEquals("Input file not modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #20: <Test  20 in file catpart.txt.tsl>
    @Test
    public void processfileTest20() throws Exception {
        String input = "First Line" + System.lineSeparator()
                + "Second linE" + System.lineSeparator()
                + "Third lIne" + System.lineSeparator();
        String expected = "1 ##First Line" + System.lineSeparator()
                + "2 ##Second linE" + System.lineSeparator()
                + "3 ##Third lIne" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-s", "line", "-n", "-i", "-p", "##", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", expected, getFileContent(inputFile.getPath()));
    }

    // Frame #21: <Test  21 in file catpart.txt.tsl>
    @Test
    public void processfileTest21() throws Exception {
        String input = "First line" + System.lineSeparator()
                + "Second linE" + System.lineSeparator()
                + "Third lIne" + System.lineSeparator();
        String expected = "1 ##First line" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-s", "line", "-n", "-p", "##", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", expected, getFileContent(inputFile.getPath()));
    }

    // Frame #22: <Test  22 in file catpart.txt.tsl>
    @Test
    public void processfileTest22() throws Exception {
        String input = "First line" + System.lineSeparator()
                + "Second linE" + System.lineSeparator()
                + "Third lIne" + System.lineSeparator();
        String expected = "##First line" + System.lineSeparator()
                + "##Second linE" + System.lineSeparator()
                + "##Third lIne" + System.lineSeparator();


        File inputFile = createInputFile(input);
        String[] args = {"-s", "line", "-i", "-p", "##", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", expected, getFileContent(inputFile.getPath()));
    }

    // Frame #23: <Test  23 in file catpart.txt.tsl>
    @Test
    public void processfileTest23() throws Exception {
        String input = "First line" + System.lineSeparator()
                + "Second linE" + System.lineSeparator()
                + "Third line" + System.lineSeparator();
        String expected = "##First line" + System.lineSeparator()
                + "##Third line" + System.lineSeparator();


        File inputFile = createInputFile(input);
        String[] args = {"-s", "line", "-p", "##", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", expected, getFileContent(inputFile.getPath()));
    }

    // Frame #24: <Test  24 in file catpart.txt.tsl>
    @Test
    public void processfileTest24() throws Exception {
        String input = "First line" + System.lineSeparator()
                + "Second line" + System.lineSeparator()
                + "Third line" + System.lineSeparator();
        String expected = "1 2First line" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-s", "first", "-n", "-i", "-p", "2", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", outStream.toString(), expected);
        assertEquals("Input not file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #25: <Test  25 in file catpart.txt.tsl>
    @Test
    public void processfileTest25() throws Exception {
        String input = "First line";
        String expected = "";

        File inputFile = createInputFile(input);
        String[] args = {"-s", "first", "-n", "-p", "2", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input not file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #26: <Test  26 in file catpart.txt.tsl>
    @Test
    public void processfileTest26() throws Exception {
        String input = "First line" + System.lineSeparator()
                + "Second line" + System.lineSeparator()
                + "Third, not Second, line" + System.lineSeparator();
        String expected = "TheSecond line" + System.lineSeparator()
                + "TheThird, not Second, line" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-s", "second", "-i", "-p", "The", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input not file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #27: <Test  27 in file catpart.txt.tsl>
    @Test
    public void processfileTest27() throws Exception {
        String input = "First line" + System.lineSeparator()
                + "Second line" + System.lineSeparator()
                + "third, not second, line" + System.lineSeparator();
        String expected = "Thethird, not second, line" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-s", "third", "-p", "The", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input not file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #28: <Test  28 in file catpart.txt.tsl>
    @Test
    public void processfileTest28() throws Exception {
        String input = "Please go Right" + System.lineSeparator()
                + "then left" + System.lineSeparator()
                + "then Right again" + System.lineSeparator();
        String expected = "1 Please go left" + System.lineSeparator()
                + "2 then left" + System.lineSeparator()
                + "3 then left again" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-n", "-r", "right", "left", "-g", "-i", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", expected, getFileContent(inputFile.getPath()));
    }

    // Frame #29: <Test  29 in file catpart.txt.tsl>
    @Test
    public void processfileTest29() throws Exception {
        String input = "Please go Right" + System.lineSeparator()
                + "then left" + System.lineSeparator()
                + "then right again" + System.lineSeparator();
        String expected = "1 Please go left" + System.lineSeparator()
                + "2 then left" + System.lineSeparator()
                + "3 then right again" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-n", "-r", "Right", "left", "-g", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", expected, getFileContent(inputFile.getPath()));
    }

    // Frame #30: <Test  30 in file catpart.txt.tsl>
    @Test
    public void processfileTest30() throws Exception {
        String input = "Please go Right" + System.lineSeparator()
                + "then left" + System.lineSeparator()
                + "then Right again" + System.lineSeparator();
        String expected = "1 Please go left" + System.lineSeparator()
                + "2 then left" + System.lineSeparator()
                + "3 then left again" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-n", "-r", "right", "left", "-i", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", expected, getFileContent(inputFile.getPath()));
    }

    // Frame #31: <Test  31 in file catpart.txt.tsl>
    @Test
    public void processfileTest31() throws Exception {
        String input = "Please go left" + System.lineSeparator()
                + "then right" + System.lineSeparator()
                + "then right again" + System.lineSeparator();
        String expected = "1 Please go left" + System.lineSeparator()
                + "2 then left" + System.lineSeparator()
                + "3 then left again" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-n", "-r", "right", "left", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", expected, getFileContent(inputFile.getPath()));
    }

    // Frame #32: <Test  32 in file catpart.txt.tsl>
    @Test
    public void processfileTest32() throws Exception {
        String input = "Please go l3ft" + System.lineSeparator()
                + "then right" + System.lineSeparator()
                + "then right again" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-r", "left", "straight", "-g", "-i", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #33: <Test  33 in file catpart.txt.tsl>
    @Test
    public void processfileTest33() throws Exception {
        String input = "Please go left" + System.lineSeparator()
                + "then right" + System.lineSeparator()
                + "then left again" + System.lineSeparator();
        String expected = "Please go straight" + System.lineSeparator()
                + "then right" + System.lineSeparator()
                + "then straight again" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-r", "left", "straight", "-g", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", expected, getFileContent(inputFile.getPath()));
    }

    // Frame #34: <Test  34 in file catpart.txt.tsl>
    @Test
    public void processfileTest34() throws Exception {
        String input = "Please go l3ft" + System.lineSeparator()
                + "then right" + System.lineSeparator()
                + "then left again" + System.lineSeparator();
        String expected = "Please go l3ft" + System.lineSeparator()
                + "then right" + System.lineSeparator()
                + "then straight again" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-r", "left", "straight", "-i", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", expected, getFileContent(inputFile.getPath()));
    }

    // Frame #35: <Test  35 in file catpart.txt.tsl>
    @Test
    public void processfileTest35() throws Exception {
        String input = "Please go straight then straight again" + System.lineSeparator()
                + "then straight" + System.lineSeparator()
                + "then straight again" + System.lineSeparator();
        String expected = "Please go backwards then straight again" + System.lineSeparator()
                + "then backwards" + System.lineSeparator()
                + "then backwards again" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-r", "straight", "backwards", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", expected, getFileContent(inputFile.getPath()));
    }

    // Frame #36: <Test  36 in file catpart.txt.tsl>
    @Test
    public void processfileTest36() throws Exception {
        String input = "Please go strAight" + System.lineSeparator()
                + "then Straight" + System.lineSeparator()
                + "then straight again" + System.lineSeparator();
        String expected = "1 Please go backwards" + System.lineSeparator()
                + "2 then backwards" + System.lineSeparator()
                + "3 then backwards again" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-n", "-r", "straight", "backwards", "-g", "-i", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input not file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #37: <Test  37 in file catpart.txt.tsl>
    @Test
    public void processfileTest37() throws Exception {
        String input = "Please go strAight" + System.lineSeparator()
                + "then straight" + System.lineSeparator()
                + "then straight again" + System.lineSeparator();
        String expected = "1 Please go strAight" + System.lineSeparator()
                + "2 then backwards" + System.lineSeparator()
                + "3 then backwards again" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-n", "-r", "straight", "backwards", "-g", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input not file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #38: <Test  38 in file catpart.txt.tsl>
    @Test
    public void processfileTest38() throws Exception {
        String input = "Please go strAight" + System.lineSeparator()
                + "then Straight" + System.lineSeparator()
                + "then straight again" + System.lineSeparator();
        String expected = "1 Please go backwards" + System.lineSeparator()
                + "2 then backwards" + System.lineSeparator()
                + "3 then backwards again" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-n", "-r", "straight", "backwards", "-i", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input not file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #39: <Test  39 in file catpart.txt.tsl>
    @Test
    public void processfileTest39() throws Exception {
        String input = "Please go strAight" + System.lineSeparator()
                + "then straight" + System.lineSeparator()
                + "then straight again" + System.lineSeparator();
        String expected = "1 Please go strAight" + System.lineSeparator()
                + "2 then backwards" + System.lineSeparator()
                + "3 then backwards again" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-n", "-r", "straight", "backwards", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input not file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #40: <Test  40 in file catpart.txt.tsl>
    @Test
    public void processfileTest40() throws Exception {
        String input = "Please go strAight" + System.lineSeparator()
                + "then straight" + System.lineSeparator()
                + "then straight again" + System.lineSeparator();
        String expected = "Please go backwards" + System.lineSeparator()
                + "then backwards" + System.lineSeparator()
                + "then backwards again" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-r", "straight", "backwards", "-g", "-i", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input not file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #41: <Test  41 in file catpart.txt.tsl>
    @Test
    public void processfileTest41() throws Exception {
        String input = "I like noodles" + System.lineSeparator()
                + "Do you also like noodles?" + System.lineSeparator()
                + "Noodles are great!" + System.lineSeparator();
        String expected = "I hate noodles" + System.lineSeparator()
                + "Do you also hate noodles?" + System.lineSeparator()
                + "Noodles are great!" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-r", "like", "hate", "-g", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input not file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #42: <Test  42 in file catpart.txt.tsl>
    @Test
    public void processfileTest42() throws Exception {
        String input = "I lik3 noodles" + System.lineSeparator()
                + "Do you also like noodles?" + System.lineSeparator()
                + "Noodles are like great!" + System.lineSeparator();
        String expected = "I lik3 noodles" + System.lineSeparator()
                + "Do you also hate noodles?" + System.lineSeparator()
                + "Noodles are hate great!" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-r", "like", "hate", "-i", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input not file modified", input, getFileContent(inputFile.getPath()));
    }

    // Frame #43: <Test  43 in file catpart.txt.tsl>
    @Test
    public void processfileTest43() throws Exception {
        String input = "I like noodles" + System.lineSeparator()
                + "Do you also lik3 noodles?" + System.lineSeparator()
                + "Noodles are like great!" + System.lineSeparator();
        String expected = "I love noodles" + System.lineSeparator()
                + "Do you also lik3 noodles?" + System.lineSeparator()
                + "Noodles are love great!" + System.lineSeparator();

        File inputFile = createInputFile(input);
        String[] args = {"-r", "like", "love", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input not file modified", input, getFileContent(inputFile.getPath()));
    }

    // Missing test scenarios
    // Scenario - 34/50
    @Test
    public void processfileTest44() throws Exception {
        //no arguments on the command line will pass an array of length 0 to the application (not a null).
        String args[]  = new String[0];
        Main.main(args);
        assertEquals("Usage: processfile [ -f | -n | -s string | -r string1 string2 | -g | -i | -p  ] FILE", errStream.toString().trim());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
    }

    // Scenario - 35/50
    @Test
    public void processfileTest45() throws Exception {
        String input = "Hey dad!";
        File inputFile = createInputFile(input);
        String[] args = {"-r", inputFile.getPath()};
        Main.main(args);
        assertEquals("Usage: processfile [ -f | -n | -s string | -r string1 string2 | -g | -i | -p  ] FILE", errStream.toString().trim());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
    }

    // Scenario - 36/50
    @Test
    public void processfileTest46() throws Exception {
        String input = "Hey dad!";
        File inputFile = createInputFile(input);
        String[] args = {"-z", inputFile.getPath()};
        Main.main(args);
        assertEquals("Usage: processfile [ -f | -n | -s string | -r string1 string2 | -g | -i | -p  ] FILE", errStream.toString().trim());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
    }

    // Scenario - 37/50
    @Test
    public void processfileTest47() throws Exception {
        String input = "This is a huge cluster";
        String expected = "1 #This is now huge cluster";

        File inputFile = createInputFile(input);
        String[] args = {"-n", "-s", "this", "-r", "a", "now", "-p", "#", "-g", "-i", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file not modified", expected, getFileContent(inputFile.getPath()));
    }
    // Scenario - 38/50
    @Test
    public void processfileTest48() throws Exception {
        String input = "I have a cow. Can I have a chicken?";

        File inputFile = createInputFile(input);
        String[] args = {"-s", "cow", "-s", "chicken", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", input, outStream.toString());
        assertEquals("Input file not modified", input, getFileContent(inputFile.getPath()));
    }

    // Scenario - 39/50
    @Test
    public void processfileTest49() throws Exception {
        String input = "I have a cow. Can I have a chicken?";
        String expected = "##I have a cow. Can I have a chicken?";

        File inputFile = createInputFile(input);
        String[] args = {"-p", "#", "-p", "##", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", expected, getFileContent(inputFile.getPath()));
    }

    // Scenario - 40/50
    @Test
    public void processfileTest50() throws Exception {
        String input = "I have a cow. Can I have a chicken?";
        String expected = "";

        File inputFile = createInputFile(input);
        String[] args = {"-s", "I \n", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", expected, outStream.toString());
        assertEquals("Input file not modified", input, getFileContent(inputFile.getPath()));
    }

    // Scenario - 41/50
    @Test
    public void processfileTest51() throws Exception {
        String input = "I have a cow. Can I have a chicken?";

        File inputFile = createInputFile(input);
        String[] args = {"-r", "I \n", "I" , inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertEquals("Unexpected stdout output", input, outStream.toString());
        assertEquals("Input file not modified", input, getFileContent(inputFile.getPath()));
    }

    // Scenario - 42/50
    @Test
    public void processfileTest52() {
        String[] args = {"-r", "valid", "invalid"};
        Main.main(args);
        assertEquals("Usage: processfile [ -f | -n | -s string | -r string1 string2 | -g | -i | -p  ] FILE", errStream.toString().trim());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
    }

    // Scenario - 43/50
    @Test
    public void processfileTest53() throws Exception {
        String input = "I have a cow. Can I have a chicken?";
        String expected = "Ihave a cow. Can I have a chicken?";

        File inputFile = createInputFile(input);
        String[] args = {"-r", " ", "", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file modified", expected, getFileContent(inputFile.getPath()));
    }

    // Scenario - 44/50
    @Test
    public void processfileTest54() throws Exception {
        String input = "This is a huge cluster";

        File inputFile = createInputFile(input);
        String[] args = {"-p", "", "-f", inputFile.getPath()};
        Main.main(args);
        assertTrue("Unexpected stderr output", errStream.toString().isEmpty());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
        assertEquals("Input file not modified", input, getFileContent(inputFile.getPath()));
    }

    // Scenario - 45/50
    @Test
    public void processfileTest55() throws Exception {
        String[] args = {""};
        Main.main(args);
        assertEquals("Usage: processfile [ -f | -n | -s string | -r string1 string2 | -g | -i | -p  ] FILE", errStream.toString().trim());
        assertTrue("Unexpected stdout output", outStream.toString().isEmpty());
    }
}