package com.travelAI.TravelAIdb.vacation;

import jakarta.persistence.*;

@Entity
@Table(name = "vacations")  // Optional, you can specify a custom table name
public class Vacation {

    @Id
    @SequenceGenerator(
            name = "vacation_sequence",
            sequenceName = "vacation_sequence",
            allocationSize = 1
    )
    @GeneratedValue(
            strategy = GenerationType.SEQUENCE,
            generator = "vacation_sequence"
    )
    private long id;

    // Changed the column name to jsonData
    @Column(name = "jsonData", columnDefinition = "TEXT")
    private String jsonData;  // This field will hold the JSON data

    // Default constructor
    public Vacation() {
    }

    // Constructor with all fields
    public Vacation(long id, String jsonData) {
        this.id = id;
        this.jsonData = jsonData;
    }

    // Constructor without the ID (for creation scenarios)
    public Vacation(String jsonData) {
        this.jsonData = jsonData;
    }

    // Overriding the toString method to include the jsonData
    @Override
    public String toString() {
        return "Vacation{" +
                "id=" + id +
                ", jsonData='" + jsonData + '\'' +
                '}';
    }

    // Getter and setter methods
    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getJsonData() {
        return jsonData;
    }

    public void setJsonData(String jsonData) {
        this.jsonData = jsonData;
    }
}
