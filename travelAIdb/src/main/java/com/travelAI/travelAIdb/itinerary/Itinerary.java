package com.travelAI.dubhacks24.itinerary;

import jakarta.persistence.*;

@Entity
@Table(name = "itinerary")  // Optional, you can specify a custom table name
public class Itinerary {

    @Id
    @SequenceGenerator(
            name = "itinerary_sequence",
            sequenceName = "itinerary_sequence",
            allocationSize = 1
    )
    @GeneratedValue(
            strategy = GenerationType.SEQUENCE,
            generator = "itinerary_sequence"
    )
    private long id;

    // Changed the column name to jsonData
    @Column(name = "jsonData", columnDefinition = "NVARCHAR(MAX)")
    private String jsonData;  // This field will hold the JSON data

    // Default constructor
    public Itinerary() {
    }

    // Constructor with all fields
    public Itinerary(long id, String jsonData) {
        this.id = id;
        this.jsonData = jsonData;
    }

    // Constructor without the ID (for creation scenarios)
    public Itinerary(String jsonData) {
        this.jsonData = jsonData;
    }

    // Overriding the toString method to include the jsonData
    @Override
    public String toString() {
        return "Itinerary{" +
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
