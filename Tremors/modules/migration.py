class Migration(object):
    """A migration event"""
    def __init__(self, eventDates, eventDistances, eventLatitudes, eventLongitudes, eventMagnitudes):
        self.eventDates = eventDates
        self.eventDistances = eventDistances
        self.eventLatitudes = eventLatitudes
        self.eventLongitudes = eventLongitudes
        self.eventMagnitudes = eventMagnitudes

        self.duration = eventDates[-1] - eventDates[0]
        self.distance = max(eventDistances) - min(eventDistances)
        self.numTremors = len(eventDates)
        self.origin = (eventLatitudes[0], eventLongitudes[0])
        self.terminus = (eventLatitudes[-1], eventLongitudes[-1])
        self.center = (sum(eventLongitudes) / len(eventLongitudes), sum(eventLatitudes) / len(eventLatitudes))
        self.minLongitude = min(eventLongitudes)
        self.minLatitude = min(eventLatitudes)
        self.maxLongitude = max(eventLongitudes)
        self.maxLatitude = max(eventLatitudes)
        
        #TODO: Figure out how to properly calculate total magnitude of the migration
        self.magnitude = sum(eventMagnitudes) / len(eventMagnitudes)

