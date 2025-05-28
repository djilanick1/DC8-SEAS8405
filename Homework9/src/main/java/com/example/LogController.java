package com.example;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.web.bind.annotation.*;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.util.regex.Pattern;

@RestController
@SpringBootApplication
public class LogController {
    private static final Logger logger = LogManager.getLogger(LogController.class);
    private static final Pattern JNDI_PATTERN = Pattern.compile("\\$\\{jndi:.*\\}", Pattern.CASE_INSENSITIVE);

    @PostMapping("/log")
    public String logInput(@RequestBody String input) {
        if (JNDI_PATTERN.matcher(input).find()) {
            logger.warn("Blocked malicious input: " + input);
            return "Blocked suspicious input!";
        }

        logger.info("User input: " + input);
        return "Logged: " + input;
    }

    public static void main(String[] args) {
        SpringApplication.run(LogController.class, args);
    }
}
