/*
 * Copyright Â© 2021 Georgia Institute of Technology (Georgia Tech). All Rights Reserved.
 * Template code for CS 6340 Software Analysis
 * Instructors: Mayur Naik and Chris Poch
 * Head TAs: Kelly Parks and Joel Cooper
 *
 * Georgia Tech asserts copyright ownership of this template and all derivative
 * works, including solutions to the projects assigned in this course. Students
 * and other users of this template code are advised not to share it with others
 * or to make it available on publicly viewable websites including repositories
 * such as GitHub and GitLab. This copyright statement should not be removed
 * or edited. Removing it will be considered an academic integrity issue.
 *
 * We do grant permission to share solutions privately with non-students such
 * as potential employers as long as this header remains in full. However, 
 * sharing with other current or future students or using a medium to share
 * where the code is widely available on the internet is prohibited and 
 * subject to being investigated as a GT honor code violation.
 * Please respect the intellectual ownership of the course materials 
 * (including exam keys, project requirements, etc.) and do not distribute them 
 * to anyone not enrolled in the class. Use of any previous semester course 
 * materials, such as tests, quizzes, homework, projects, videos, and any other 
 * coursework, is prohibited in this course. */
 
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.List;
import java.util.Arrays;

public class DeltaDebug {
	private List<String> minimizeAlgorithm(List<String> lineList, String programName, String errorMessage, Boolean isChar) {
		List<String> delta = new ArrayList<String>();
		List<String> extraDelta = new ArrayList<String>();
		List<String> lineDelta = lineList;
		String charDelta  = "";
		
		if(isChar) { charDelta = flattenList(lineDelta); }

		int n = 2;
		int deltaLength = isChar ? charDelta.length() : lineDelta.size();

		while(n <= deltaLength) {
			List<List<String>> tempDeltaPartitions = new ArrayList<List<String>>();
			// Split delta
			if(isChar) {
				tempDeltaPartitions = createCharTemporaryDeltaPartitions(charDelta, n);
			} else {
				tempDeltaPartitions = createLineTemporaryDeltaPartitions(lineDelta, n);
			}

			// Finialize delta lists
			List<List<String>> deltaPartitions = finalizeDeltaPartitions(tempDeltaPartitions, n);		
				
			// Set nebula
			List<List<String>> nebulas = setNebulas(deltaPartitions);
			
			// Update n
			delta = isChar ? Arrays.asList(charDelta) : lineDelta;
			List<String> updatedDelta = updateDelta(nebulas, delta, programName, errorMessage, isChar);
			n = updateN(delta.equals(updatedDelta), n);

			// Update Delta
			delta = updatedDelta;

			// Check if n is greater than length
			if(n > deltaLength) {
				if(delta.equals(extraDelta)) {
					break;
				} else {
					extraDelta = delta;
					n = deltaLength;
				}
			}
	
			// Update line or char deltas
			if(isChar) {
				charDelta = flattenList(delta);
				deltaLength = charDelta.length();
			} else {
				lineDelta = delta;
				deltaLength = lineDelta.size(); 
			}
		}

		return delta;
	}

	private int updateN(Boolean similar, int n) {
		if(similar) {
			n *= 2;
		} else {
			n -= 1;
		}
		
		return n;
	}

	private List<List<String>> createLineTemporaryDeltaPartitions(List<String> lineDelta, int n) {
		List<List<String>> tempDeltaPartitions = new ArrayList<List<String>>();
		int partitions = lineDelta.size() / n;

		//Source: https://stackoverflow.com/questions/2895342/java-how-can-i-split-an-arraylist-in-multiple-small-arraylists
		for(int i = 0; i < lineDelta.size(); i += partitions) {
			List<String> deltaSubList = lineDelta.subList(i, Math.min(lineDelta.size(), i + partitions));
			tempDeltaPartitions.add(deltaSubList);
		}
		return tempDeltaPartitions;
	}

	private List<List<String>> createCharTemporaryDeltaPartitions(String charDelta, int n) {
		List<List<String>> tempDeltaPartitions = new ArrayList<List<String>>();
		int partitions = charDelta.length() / n;
		
		for(int i = 0; i < charDelta.length(); i += partitions) {
			List<String> deltaSubList = Arrays.asList(charDelta.substring(i, Math.min(charDelta.length(), i + partitions)));
			tempDeltaPartitions.add(deltaSubList);
		}
		
		return tempDeltaPartitions;
	}

	private String flattenList(List<String> lineList) {
		String stringDelta = "";
		for (int i = 0; i < lineList.size(); i++) {
			stringDelta += lineList.get(i);
		}
		return stringDelta;
	}

	private List<List<String>> finalizeDeltaPartitions(List<List<String>> tempDeltaPartitions, int n) {
		List<List<String>> deltaPartitions = new ArrayList<List<String>>();
		if(tempDeltaPartitions.size() > n) {
			List<String> finalPartition = new ArrayList<String>();
			for(int i = 0; i < tempDeltaPartitions.size(); i++) {
				if((i + 1) >= n) {
					finalPartition.addAll(tempDeltaPartitions.get(i));
				} else {
					deltaPartitions.add(tempDeltaPartitions.get(i));
				}
			}
			deltaPartitions.add(finalPartition);
		} else {
			deltaPartitions = tempDeltaPartitions;
		}
		return deltaPartitions;
	}
	
	private List<List<String>> setNebulas(List<List<String>> deltas) {
		List<List<String>> nebulas = new ArrayList<List<String>>();
		for (int i = 0; i < deltas.size(); i++) {
			List<String> tempNebula = createNebula(deltas, i);
			nebulas.add(tempNebula);
		}
		return nebulas;
	}

	private List<String> createNebula(List<List<String>> deltas, int iteration) {
		List<String> nebula = new ArrayList<String>();
		for(int i = 0; i < deltas.size(); i++) {
			if((i != iteration)) {
				nebula.addAll(deltas.get(i));
			}
		}
		return nebula;
	}

	private List<String> updateDelta(List<List<String>> nebulas, List<String> delta, String programName, String errorMessage, Boolean isChar) {
		for(int i = 0; i < nebulas.size(); i++) {
			boolean failure = runCommand(programName, nebulas.get(i), errorMessage, isChar);
			if(failure) {
				return nebulas.get(i);
			}
		}
		return delta;
	}

	/**
	 * deltaDebug is the method is what will run the delta debug algorithm
	 * !!!!!! IMPORTANT: DO NOT CHANGE THE TYPE/METHOD SIGNATURE AS IT MUST BE THE SAME AS PROVIDED FOR GRADING !!!!!!  
	 * @param char_granularity - if false, use line granularity for the algorithm
	 * @param program - the path of the program you're testing, e.g. "./SecretCoder"
	 * @param failing_file - path of provided failing input file, e.g. "./input_file.txt"
	 * @param error_msg - the program output that Delta should treat as an error, e.g. "java.lang.ArrayIndexOutOfBoundsException"
	 * @param final_minimized_file - path to write minimized output file to  
	 */
	public void deltaDebug(Boolean char_granularity, String program, String failing_file, String error_msg, String final_minimized_file)
	{
		// Transform input file into list of strings
		List<String> originalFileList = readFile(failing_file);
		
		// Get line granularity from input file
		List<String> finalMinimizedList = new ArrayList<String>();
		
		// Get line or char granularity
		finalMinimizedList = minimizeAlgorithm(originalFileList, program, error_msg, char_granularity);
		
		// Write finalized list 
		writeToFile(final_minimized_file, finalMinimizedList);
	}
	
	/**
	 * readFile reads input from a file line by line
	 * You can update this method to pass in more parameters or return something if needed
	 * @param file - file to read
	 */
	public List<String> readFile(String file)
	{
		Scanner scan;
		List<String> initalFileLines = new ArrayList<String>();
		try {
			scan = new Scanner(new File(file));
			while (scan.hasNextLine()){
				initalFileLines.add(scan.nextLine());
			}
			scan.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		return initalFileLines;
	}
	
	/**
	 * runCommand can be used to run a program 
	 * You can update this method to pass in more/different parameters or return something if needed
	 * @param command - complete command you want to run (program location + any command args)
	 * @param error - error message you're looking for
	 */
	public boolean runCommand(String command, List<String> nebula, String error_msg, Boolean isChar)
	{
		String s = null;
		String tempFile = "temp_failing_file_check.txt";
		writeToFile(tempFile, isChar ? Arrays.asList(flattenList(nebula)) : nebula);
		try{ 	
            Process p = Runtime.getRuntime().exec(command + " " + tempFile);
            
            BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getErrorStream()));
            // read the output from the command
            while ((s = stdInput.readLine()) != null) {
			    if (s.contains(error_msg)) {
					return true;
				}
            }
		}
		catch (IOException e) {
            System.out.println(command + "failed to run");
            System.exit(-1);
        }
		return false;
	}

	/**
     * writeFile() can be used to write to a file
     * This is a basic method for writing your String to a file
     * You can use helper methods to call on this method if you wish, but we do not recommend modifying 
     * this method directly. 
     * @param file - file to write to
     * @param List<String> - abstract data structure for holding String objects, you can pass in an ArrayList<String>, for example
     */
    public boolean writeToFile(String file, List<String> list)
    {
        Path out = Paths.get(file);
        try {
            Files.write(out,list,Charset.defaultCharset());
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }		
	

}

