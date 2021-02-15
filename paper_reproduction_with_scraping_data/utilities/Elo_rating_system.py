class Elo_rating_system:
    """
    A class that represents an implementation of the Elo Rating System with some changes from https://github.com/HankSheehan/EloPy
    """

    def __init__(self, base_rating=1000):
        """
        Runs at initialization of class object.
        @param base_rating - The rating a new player would have
        """
        self.base_rating = base_rating
        self.team = []

    def __getTeamList(self):
        """
        Returns this implementation's player list.
        @return - the list of all player objects in the implementation.
        """
        return self.team

    def getTeam(self, name):
        """
        Returns the player in the implementation with the given name.
        @param name - name of the player to return.
        @return - the player with the given name.
        """
        for team in self.team:
            if team.name == name:
                return team
        return None

    def contains(self, name):
        """
        Returns true if this object contains a player with the given name.
        Otherwise returns false.
        @param name - name to check for.
        """
        for team in self.team:
            if team.name == name:
                return True
        return False

    def addTeam(self, name, rating=None):
        """
        Adds a new player to the implementation.
        @param name - The name to identify a specific player.
        @param rating - The player's rating.
        """
        if rating == None:
            rating = self.base_rating

        self.team.append(_Team(name=name,rating=rating))

    def removeTeam(self, name):
        """
        Adds a new player to the implementation.
        @param name - The name to identify a specific player.
        """
        self.__getTeamList().remove(self.getTeam(name))


    def recordMatch(self, name1, name2,k0,lamda,winner=None,diff=None):
        """
        Should be called after a game is played.
        @param name1 - name of the first player.
        @param name2 - name of the second player.
        """
        team1 = self.getTeam(name1)
        team2 = self.getTeam(name2)

        expected1 = team1.compareRating(team2)
        expected2 = team2.compareRating(team1)
        
        k = k0*(1+abs(diff))**lamda
        
        rating1 = team1.rating
        rating2 = team2.rating

        if winner == name1:
            score1 = 1.0
            score2 = 0.0
        elif winner == name2:
            score1 = 0.0
            score2 = 1.0

        newRating1 = rating1 + k * (score1 - expected1)
        newRating2 = rating2 + k * (score2 - expected2)


        team1.rating = newRating1
        team2.rating = newRating2

    def getTeamRating(self, name):
        """
        Returns the rating of the player with the given name.
        @param name - name of the player.
        @return - the rating of the player with the given name.
        """
        team = self.getTeam(name)
        return team.rating

    def getRatingList(self):
        """
        Returns a list of tuples in the form of ({name},{rating})
        @return - the list of tuples
        """
        lst = []
        for team in self.__getTeamList():
            lst.append((team.name,team.rating))
        return lst

class _Team:
    """
    A class to represent a player in the Elo Rating System
    """

    def __init__(self, name, rating):
        """
        Runs at initialization of class object.
        @param name - TODO
        @param rating - TODO
        """
        self.name = name
        self.rating = rating

    def compareRating(self, opponent):
        """
        Compares the two ratings of the this player and the opponent.
        @param opponent - the player to compare against.
        @returns - The expected score between the two players.
        """
        return ( 1+10**( ( opponent.rating-self.rating )/400.0 ) ) ** -1