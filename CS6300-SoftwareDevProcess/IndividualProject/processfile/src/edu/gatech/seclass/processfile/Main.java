package edu.gatech.seclass.processfile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.InvalidPathException;
import java.nio.file.Path;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Main {
    private static String[] parameters;
    public static void main(String[] args) {
        parameters = args;
        String filePath;
        HashMap<String, Boolean> optionStatus = new HashMap<>();
        boolean file;

        try {
           filePath = parameters[parameters.length - 1];
           file = checkFile(filePath);
            if(file) {
                String fileContent = Files.readString(Path.of(filePath)), sInput, pInput;
                List<String> rInputs;
                removeOptions(Arrays.asList(filePath), parameters);
                createOptionsHashMap(optionStatus, parameters);
                boolean f = optionStatus.get("-f"), s = optionStatus.get("-s"), r = optionStatus.get("-r"),
                        p = optionStatus.get("-p"), n = optionStatus.get("-n"), g = optionStatus.get("-g"),
                        i = optionStatus.get("-i"), stdout = true, stderr = false;
               if(f) {
                   stdout = false;
                   removeOptions(Arrays.asList("-f"), parameters);
               }
               if(g) {
                   if(r) {
                       removeOptions(Arrays.asList("-g"), parameters);
                   } else {
                       stderr = true;
                   }
               }
               if(i) {
                   if(s || r) {
                       removeOptions(Arrays.asList("-i"), parameters);
                   } else {
                       stderr = true;
                   }
               }
               if(s) {
                   try {
                       int sIndex = Arrays.asList(parameters).indexOf("-s");
                       sInput = parameters[sIndex + 1];

                       fileContent = sFlag(fileContent, sInput, i);
                       removeOptions(Arrays.asList("-s", sInput), parameters);
                   } catch (IndexOutOfBoundsException e) {
                       stderr = true;
                   }
               }
               if(r) {
                   try {
                       int rIndex = Arrays.asList(parameters).indexOf("-r");
                       rInputs = Arrays.asList(parameters[rIndex + 1], parameters[rIndex + 2]);

                       fileContent = rFlag(fileContent, rInputs, g, i);
                       removeOptions(Arrays.asList("-r", rInputs.get(0), rInputs.get(1)), parameters);
                   } catch (IndexOutOfBoundsException e) {
                       stderr = true;
                   }
               }
               if(p) {
                   try {
                       int pIndex = Arrays.asList(parameters).indexOf("-p");
                       pInput = parameters[pIndex + 1];

                       fileContent = pFlag(fileContent, pInput);
                       removeOptions(Arrays.asList("-p", pInput), parameters);
                   } catch (IndexOutOfBoundsException e) {
                       stderr = true;
                   }
               }
               if(n) {
                   fileContent = nFlag(fileContent);
                   removeOptions(Arrays.asList("-n"), parameters);
               }
               if(stderr || parameters.length > 0) {
                   usage();
               } else {
                   if(stdout) {
                       System.out.print(fileContent);
                   } else {
                       Files.writeString(Path.of(filePath), fileContent);
                   }
               }
            } else {
                usage();
            }
        } catch (ArrayIndexOutOfBoundsException | IOException e) {
            usage();
        }
    }

    private static void usage() {
        System.err.println("Usage: processfile [ -f | -n | -s string | -r string1 string2 | -g | -i | -p  ] FILE");
    }

    private static boolean checkFile(String filePath) {
        try {
            return Files.exists(Path.of(filePath));
        } catch (InvalidPathException e) {
            return false;
        }
    }

    private static boolean checkFlag(String flag, String[] options) {
        int count = 0;
        for(String option : options) {
           if(option.equals(flag)) {
               count++;
           }
        }
        return checkDuplicates(flag, count);
    }

    private static boolean checkDuplicates(String flag, int count){
        if(count == 1) {
            return true;
        } else if(count == 2) {
            try {
                int index = Arrays.asList(parameters).indexOf(flag);
                if(flag.equals("-s") || flag.equals("-p")) {
                    removeOptions(Arrays.asList(flag, parameters[index + 1]), parameters);
                } else if(flag.equals("-r")) {
                    removeOptions(Arrays.asList(flag, parameters[index + 1], parameters[index + 2]), parameters);
                }
                return true;
            } catch (IndexOutOfBoundsException e) {
                usage();
            }
        } else if(count > 2) {
            usage();
        }
        return false;
    }

    private static void removeOptions(List<String> params, String[] options) {
        List<String> editParams = new ArrayList<>(Arrays.asList(options));
        for(String param : params) {
            editParams.remove(param);
        }
        parameters = editParams.toArray(new String[0]);
    }

    private static void createOptionsHashMap(HashMap<String, Boolean> optionStatus, String[] args) {
        optionStatus.put("-f", checkFlag("-f", args));
        optionStatus.put("-i", checkFlag("-i", args));
        optionStatus.put("-g", checkFlag("-g", args));
        optionStatus.put("-s", checkFlag("-s", args));
        optionStatus.put("-r", checkFlag("-r", args));
        optionStatus.put("-p", checkFlag("-p", args));
        optionStatus.put("-n", checkFlag("-n", args));
    }

    private static String checkSpecialCharacters(String input) {
        String specialCharacters="!#$%&'()*+,-./:;<=>?@[]^_`{|}";
        Pattern pattern = Pattern.compile("[^a-zA-Z0-9 ]");
        Matcher matcher = pattern.matcher(input);
        boolean doesStringContainsSC = matcher.find();
        StringBuilder modifiedInput = new StringBuilder();

        if (doesStringContainsSC) {
            for(int i=0; i < input.length(); i++) {
                if (specialCharacters.contains(Character.toString(input.charAt(i)))) {
                    modifiedInput.append("\\").append(input.charAt(i));
                } else {
                    modifiedInput.append(i);
                }
            }
        } else {
            modifiedInput.append(input);
        }
        return modifiedInput.toString();
    }

    private static String sFlag(String fileContent, String input, boolean iFlag) {
        StringBuilder newFileContent = new StringBuilder();

        if(input.isEmpty()) {
            newFileContent.append(fileContent);
        } else {
            String[] lineContent = fileContent.split("(?<=" + System.lineSeparator() +  ")");
            for(String line : lineContent) {
                if(!line.isEmpty()) {
                    if(iFlag ? line.toLowerCase().contains(input.toLowerCase()) : line.contains(input)) {
                        newFileContent.append(line);
                    }
                }
            }
        }
        return newFileContent.toString();
    }

    private static String rFlag(String fileContent, List<String> inputs, boolean gFlag, boolean iFlag) {
        StringBuilder newFileContent = new StringBuilder();
        String input1 = checkSpecialCharacters(inputs.get(0)),input2 = checkSpecialCharacters(inputs.get(1));

        if(input1.isEmpty()) {
            usage();
        } else {
            String[] lineContent = fileContent.split("(?<=" + System.lineSeparator() +  ")");
            for(String line : lineContent) {
                if(!line.isEmpty()) {
                    if (iFlag) { input1 = "(?i)" + input1; }
                    line = gFlag ? line.replaceAll(input1, input2) : line.replaceFirst(input1, input2);
                }
                newFileContent.append(line);
            }
        }
        return newFileContent.toString();
    }

    private static String pFlag(String fileContent, String input) {
        StringBuilder newFileContent = new StringBuilder();
        String[] lineContent = fileContent.split("(?<=" + System.lineSeparator() +  ")");

        for(String line : lineContent) {
            if(!line.isEmpty()) {
                line = input + line;
                newFileContent.append(line);
            }
        }
        return newFileContent.toString();
    }

    private static String nFlag(String fileContent) {
        int count = 1;
        StringBuilder newFileContent = new StringBuilder();
        String[] lineContent = fileContent.split("(?<=" + System.lineSeparator() +  ")");
        for(String line : lineContent) {
            if(!line.isEmpty()) {
                line = count + " " + line;
                newFileContent.append(line);
                count++;
            }
        }
        return newFileContent.toString();
    }
}
