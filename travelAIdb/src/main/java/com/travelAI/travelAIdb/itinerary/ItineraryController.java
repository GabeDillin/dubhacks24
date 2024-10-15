package com.travelAI.TravelAIdb.itinerary;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("api/v1/itineraries")
public class ItineraryController {
    private final ItineraryService itineraryService;

    @Autowired
    public ItineraryController(ItineraryService itineraryService) {
        this.itineraryService = itineraryService;
    }

    // Get all itineraries
    @CrossOrigin(origins = "http://localhost:3000")
    @GetMapping
    public List<Itinerary> getItineraries() {
        return itineraryService.getItineraries();
    }

    // Add a new itinerary with JSON data
    @CrossOrigin(origins = "http://localhost:3000")
    @PostMapping
    public void addItinerary(@RequestBody String jsonData) {
        // Creating a new Itinerary object with the provided jsonData
        Itinerary itinerary = new Itinerary(jsonData);
        itineraryService.addItinerary(itinerary);
    }

    // Delete an itinerary by ID
    @CrossOrigin(origins = "http://localhost:3000")
    @DeleteMapping(path = "{itineraryId}")
    public void deleteItinerary(@PathVariable("itineraryId") Long itineraryId) {
        itineraryService.deleteItinerary(itineraryId);
    }

    // Update an existing itinerary's JSON data
    @CrossOrigin(origins = "http://localhost:3000")
    @PutMapping(path = "{itineraryId}")
    public void updateItinerary(@PathVariable("itineraryId") Long itineraryId,
                                @RequestBody String jsonData) {
        itineraryService.updateItinerary(itineraryId, jsonData);
    }
}
