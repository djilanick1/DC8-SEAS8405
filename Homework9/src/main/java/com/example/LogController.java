package com.example;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.web.bind.annotation.*;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@RestController
public class LogController {
    private static final Logger logger = LogManager.getLogger(LogController.class);

    @PostMapping("/log")
    public String logInput(@RequestBody String input) {
        logger.info("User input: " + input);
        return "Logged: " + input;
    }
}

@SpringBootApplication
public class LogController {
    public static void main(String[] args) {
        SpringApplication.run(LogController.class, args);
    }
}
