package net.bobbo.dmtflcocktail.data;

public class BandcampAlbum {

  private String albumURL;
  private BandcampTrack[] tracks;


  public BandcampAlbum(String albumURL) {
    this.albumURL = albumURL;
    this.tracks = new BandcampTrack[0];
  }


  public String getAlbumURL() {
    return albumURL;
  }

  public int getTrackCount() {
    return tracks.length;
  }

  public void addTrackToAlbum(BandcampTrack newTrack) {
    // Create new array to replace tracks
    BandcampTrack[] newTracks = new BandcampTrack[tracks.length + 1];

    // Fill the new array with the existing tracks
    for(int i = 0; i < tracks.length; i++) {
      newTracks[i] = tracks[i];
    }

    // Add new track to the end of the new array
    newTracks[tracks.length] = newTrack;

    // Apply the new array
    tracks = newTracks;
  }

}
