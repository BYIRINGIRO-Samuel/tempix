#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

// --- Configuration ---
// Candidate Name (Change this if needed)
String candidateName = "BYIRINGIRO Samuel";

// DHT Sensor Configuration
#define DHTPIN 2       // Digital pin connected to the DHT sensor 'S' pin
#define DHTTYPE DHT11  // DHT 11
DHT dht(DHTPIN, DHTTYPE);

// LCD Configuration (I2C address is usually 0x27 or 0x3F)
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Scrolling Variables
int scrollCursor = 0;
unsigned long lastScrollTime = 0;
const int scrollDelay = 300; // ms between scrolls
String paddedName;

unsigned long lastReadTime = 0;
const int readInterval = 2000; // Read sensor every 2 seconds
float currentTemp = 0.0;

void setup() {
  // Initialize Serial for PC Communication
  Serial.begin(9600);
  
  // Initialize Sensor
  dht.begin();
  
  // Initialize LCD
  lcd.init();
  lcd.backlight();
  
  // Pad the name with spaces for smooth scrolling if it's longer than 16 chars
  if (candidateName.length() > 16) {
    paddedName = candidateName + "                ";
  } else {
    paddedName = candidateName;
  }
}

void loop() {
  unsigned long currentMillis = millis();
  
  // 1. Read Temperature Data
  if (currentMillis - lastReadTime >= readInterval) {
    lastReadTime = currentMillis;
    
    // Read temperature as Celsius
    float temp = dht.readTemperature();
    
    // Check if any reads failed and exit early (to try again).
    if (!isnan(temp)) {
      currentTemp = temp;
      
      // Send data to PC via Serial Communication
      // Format: TEMP:25.50
      Serial.print("TEMP:");
      Serial.println(currentTemp);
      
      // Update the second row of the LCD
      lcd.setCursor(0, 1);
      lcd.print("Temp: ");
      lcd.print(currentTemp);
      lcd.print(" C    "); // Spaces to clear old characters
    } else {
      Serial.println("ERROR: Failed to read from DHT sensor!");
    }
  }
  
  // 2. Handle Scrolling Name on First Row
  if (candidateName.length() > 16) {
    if (currentMillis - lastScrollTime >= scrollDelay) {
      lastScrollTime = currentMillis;
      
      lcd.setCursor(0, 0);
      lcd.print(paddedName.substring(scrollCursor, scrollCursor + 16));
      
      scrollCursor++;
      if (scrollCursor > candidateName.length()) {
        scrollCursor = 0;
      }
    }
  } else {
    // If name is <= 16 chars, just print it once (or repeatedly without scrolling)
    lcd.setCursor(0, 0);
    lcd.print(candidateName);
  }
}
