#include <stdio.h>
#include <fcntl.h>  // For open()
#include <unistd.h> // For write(), close()
#include <string.h> // For strlen()

// Function prototypes
void readFile(int log_fd);
void processData(int log_fd);
void filterData(int log_fd);
void handleData(int log_fd);
void validateData(int log_fd);
void finalize(int log_fd);
void logMessage(int log_fd, const char *message);
void saveResults(int log_fd);
void cleanup(int log_fd);
void logError(int log_fd);

// Function definitions

void readFile(int log_fd) {
    logMessage(log_fd, "Reading data from file...\n");
    processData(log_fd);  // readFile calls processData
}

void processData(int log_fd) {
    logMessage(log_fd, "Processing data...\n");
    filterData(log_fd);  // processData calls filterData
}

void filterData(int log_fd) {
    logMessage(log_fd, "Filtering data...\n");
    handleData(log_fd);  // filterData calls handleData
}

void handleData(int log_fd) {
    logMessage(log_fd, "Handling filtered data...\n");
    validateData(log_fd);  // handleData calls validateData
}

void validateData(int log_fd) {
    logMessage(log_fd, "Validating data...\n");
    finalize(log_fd);  // validateData calls finalize
}

void finalize(int log_fd) {
    logMessage(log_fd, "Finalizing and saving results...\n");
}

void saveResults(int log_fd) {
    logMessage(log_fd, "Saving results to file...\n");
    cleanup(log_fd);  // saveResults calls cleanup
}

void cleanup(int log_fd) {
    logMessage(log_fd, "Cleaning up resources...\n");
    logError(log_fd);  // cleanup calls logError
}

void logError(int log_fd) {
    logMessage(log_fd, "Logging any errors...\n");
    processData(log_fd);  // logError calls processData (recursive behavior)
}

// Utility function to log messages to a file using syscalls
void logMessage(int log_fd, const char *message) {
    write(log_fd, message, strlen(message));
}

int main() {
    // Open the log file using the open syscall (O_CREAT creates the file if it doesn't exist)
    int log_fd = open("process_log.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    
    if (log_fd < 0) {
        perror("Failed to open log file");
        return 1;
    }

    // Start processing and logging
    readFile(log_fd);  // Start by reading a file
    saveResults(log_fd);  // Save results after processing data

    // Close the log file
    close(log_fd);
    
    return 0;
}
