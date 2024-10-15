package com.travelAI.dubhacks24.itinerary;

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
    @GetMapping
    public List<Itinerary> getItineraries() {
        return itineraryService.getItineraries();
    }

    // Add a new itinerary with JSON data
    @PostMapping
    public void addItinerary(@RequestBody String jsonData) {
        // Creating a new Itinerary object with the provided jsonData
        Itinerary itinerary = new Itinerary(jsonData);
        itineraryService.addItinerary(itinerary);
    }

    // Delete an itinerary by ID
    @DeleteMapping(path = "{itineraryId}")
    public void deleteItinerary(@PathVariable("itineraryId") Long itineraryId) {
        itineraryService.deleteItinerary(itineraryId);
    }

    // Update an existing itinerary's JSON data
    @PutMapping(path = "{itineraryId}")
    public void updateItinerary(@PathVariable("itineraryId") Long itineraryId,
                                @RequestBody String jsonData) {
        itineraryService.updateItinerary(itineraryId, jsonData);
    }
}
