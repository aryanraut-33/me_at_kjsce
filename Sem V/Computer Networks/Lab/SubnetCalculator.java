import java.util.*;

public class SubnetCalculator {
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("=== IP Classes and Subnet Mask Calculator ===");
        
        // Get IP address from user
        System.out.print("Enter IP address (e.g., 192.168.1.100): ");
        String ipAddress = scanner.nextLine();
        
        // Get number of required subnets
        System.out.print("Enter number of subnets required: ");
        int requiredSubnets = scanner.nextInt();
        
        try {
            // Parse and validate IP address
            int[] ipOctets = parseIPAddress(ipAddress);
            
            // Determine IP class and default subnet mask
            char ipClass = determineIPClass(ipOctets[0]);
            int[] defaultSubnetMask = getDefaultSubnetMask(ipClass);
            
            System.out.println("\n=== IP Address Analysis ===");
            System.out.println("IP Address: " + ipAddress);
            System.out.println("IP Class: Class " + ipClass);
            System.out.println("Default Subnet Mask: " + arrayToIP(defaultSubnetMask));
            System.out.println("Default Subnet Mask (Binary): " + ipToBinary(defaultSubnetMask));
            
            // Calculate required subnet bits
            int subnetBits = calculateSubnetBits(requiredSubnets);
            System.out.println("\nSubnet Bits Required: " + subnetBits);
            
            // Calculate custom subnet mask
            int[] customSubnetMask = calculateCustomSubnetMask(ipClass, subnetBits);
            int cidrNotation = calculateCIDR(customSubnetMask);
            
            System.out.println("\n=== Subnet Calculation Results ===");
            System.out.println("Custom Subnet Mask: " + arrayToIP(customSubnetMask));
            System.out.println("Custom Subnet Mask (Binary): " + ipToBinary(customSubnetMask));
            System.out.println("CIDR Notation: /" + cidrNotation);
            
            // Calculate subnet details
            int actualSubnets = (int) Math.pow(2, subnetBits);
            int hostBits = 32 - cidrNotation;
            int hostsPerSubnet = (int) Math.pow(2, hostBits) - 2; // -2 for network and broadcast
            
            System.out.println("Number of Subnets: " + actualSubnets);
            System.out.println("Hosts per Subnet: " + hostsPerSubnet);
            System.out.println("Total Usable Hosts: " + (actualSubnets * hostsPerSubnet));
            
            // Calculate and display subnet addresses
            System.out.println("\n=== Subnet Addresses ===");
            calculateSubnetAddresses(ipOctets, customSubnetMask, actualSubnets, hostsPerSubnet);
            
            // Show example calculation with AND operation
            System.out.println("\n=== Example: Bitwise AND Operation ===");
            demonstrateANDOperation(ipOctets, customSubnetMask);
            
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
        
        scanner.close();
    }
    
    // Parse IP address string into integer array
    public static int[] parseIPAddress(String ip) throws Exception {
        String[] parts = ip.split("\\.");
        if (parts.length != 4) {
            throw new Exception("Invalid IP address format");
        }
        
        int[] octets = new int[4];
        for (int i = 0; i < 4; i++) {
            octets[i] = Integer.parseInt(parts[i]);
            if (octets[i] < 0 || octets[i] > 255) {
                throw new Exception("Invalid octet value: " + octets[i]);
            }
        }
        return octets;
    }
    
    // Determine IP class based on first octet
    public static char determineIPClass(int firstOctet) {
        if (firstOctet >= 1 && firstOctet <= 126) {
            return 'A';
        } else if (firstOctet >= 128 && firstOctet <= 191) {
            return 'B';
        } else if (firstOctet >= 192 && firstOctet <= 223) {
            return 'C';
        } else if (firstOctet >= 224 && firstOctet <= 239) {
            return 'D';
        } else {
            return 'E';
        }
    }
    
    // Get default subnet mask for IP class
    public static int[] getDefaultSubnetMask(char ipClass) {
        switch (ipClass) {
            case 'A':
                return new int[]{255, 0, 0, 0};
            case 'B':
                return new int[]{255, 255, 0, 0};
            case 'C':
                return new int[]{255, 255, 255, 0};
            default:
                return new int[]{255, 255, 255, 0}; // Default to Class C
        }
    }
    
    // Calculate minimum bits required for subnets
    public static int calculateSubnetBits(int requiredSubnets) {
        return (int) Math.ceil(Math.log(requiredSubnets) / Math.log(2));
    }
    
    // Calculate custom subnet mask with additional subnet bits
    public static int[] calculateCustomSubnetMask(char ipClass, int subnetBits) {
        int[] defaultMask = getDefaultSubnetMask(ipClass);
        int defaultCIDR = (ipClass == 'A') ? 8 : (ipClass == 'B') ? 16 : 24;
        int newCIDR = defaultCIDR + subnetBits;
        
        return cidrToSubnetMask(newCIDR);
    }
    
    // Convert CIDR notation to subnet mask
    public static int[] cidrToSubnetMask(int cidr) {
        int[] mask = new int[4];
        int remainingBits = cidr;
        
        for (int i = 0; i < 4; i++) {
            if (remainingBits >= 8) {
                mask[i] = 255;
                remainingBits -= 8;
            } else if (remainingBits > 0) {
                mask[i] = (0xFF << (8 - remainingBits)) & 0xFF;
                remainingBits = 0;
            } else {
                mask[i] = 0;
            }
        }
        return mask;
    }
    
    // Calculate CIDR notation from subnet mask
    public static int calculateCIDR(int[] subnetMask) {
        int cidr = 0;
        for (int octet : subnetMask) {
            cidr += Integer.bitCount(octet);
        }
        return cidr;
    }
    
    // Calculate all subnet addresses
    public static void calculateSubnetAddresses(int[] ipAddress, int[] subnetMask, int numSubnets, int hostsPerSubnet) {
        // Calculate network address (IP AND SubnetMask)
        int[] networkAddress = performAND(ipAddress, subnetMask);
        
        // Calculate subnet increment
        int subnetIncrement = hostsPerSubnet + 2; // +2 for network and broadcast addresses
        
        System.out.printf("%-15s %-15s %-15s %-15s%n", "Subnet #", "Network Address", "First Host", "Last Host", "Broadcast");
        System.out.println("-------------------------------------------------------------------------");
        
        for (int i = 0; i < Math.min(numSubnets, 10); i++) { // Show first 10 subnets
            int[] currentNetwork = addToIP(networkAddress, i * subnetIncrement);
            int[] firstHost = addToIP(currentNetwork, 1);
            int[] lastHost = addToIP(currentNetwork, hostsPerSubnet);
            int[] broadcast = addToIP(currentNetwork, hostsPerSubnet + 1);
            
            System.out.printf("%-15d %-15s %-15s %-15s %-15s%n", 
                (i + 1), 
                arrayToIP(currentNetwork),
                arrayToIP(firstHost),
                arrayToIP(lastHost),
                arrayToIP(broadcast));
        }
        
        if (numSubnets > 10) {
            System.out.println("... (showing first 10 subnets only)");
        }
    }
    
    // Perform bitwise AND operation
    public static int[] performAND(int[] ip, int[] mask) {
        int[] result = new int[4];
        for (int i = 0; i < 4; i++) {
            result[i] = ip[i] & mask[i];
        }
        return result;
    }
    
    // Add value to IP address
    public static int[] addToIP(int[] ip, int value) {
        long ipValue = ((long)ip[0] << 24) + ((long)ip[1] << 16) + ((long)ip[2] << 8) + ip[3];
        ipValue += value;
        
        return new int[] {
            (int)((ipValue >> 24) & 0xFF),
            (int)((ipValue >> 16) & 0xFF),
            (int)((ipValue >> 8) & 0xFF),
            (int)(ipValue & 0xFF)
        };
    }
    
    // Demonstrate AND operation with binary representation
    public static void demonstrateANDOperation(int[] ip, int[] mask) {
        System.out.println("IP Address:    " + arrayToIP(ip) + " = " + ipToBinary(ip));
        System.out.println("Subnet Mask:   " + arrayToIP(mask) + " = " + ipToBinary(mask));
        
        int[] networkAddress = performAND(ip, mask);
        System.out.println("Network Addr:  " + arrayToIP(networkAddress) + " = " + ipToBinary(networkAddress));
        
        System.out.println("\nBitwise AND Operation:");
        for (int i = 0; i < 4; i++) {
            System.out.printf("Octet %d: %s & %s = %s%n", 
                (i + 1),
                String.format("%8s", Integer.toBinaryString(ip[i])).replace(' ', '0'),
                String.format("%8s", Integer.toBinaryString(mask[i])).replace(' ', '0'),
                String.format("%8s", Integer.toBinaryString(networkAddress[i])).replace(' ', '0'));
        }
    }
    
    // Convert IP array to string
    public static String arrayToIP(int[] ip) {
        return ip[0] + "." + ip[1] + "." + ip[2] + "." + ip[3];
    }
    
    // Convert IP to binary representation
    public static String ipToBinary(int[] ip) {
        StringBuilder binary = new StringBuilder();
        for (int i = 0; i < 4; i++) {
            if (i > 0) binary.append(".");
            binary.append(String.format("%8s", Integer.toBinaryString(ip[i])).replace(' ', '0'));
        }
        return binary.toString();
    }
}