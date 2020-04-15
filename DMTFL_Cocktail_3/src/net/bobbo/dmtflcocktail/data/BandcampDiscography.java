package net.bobbo.dmtflcocktail.data;

public class BandcampDiscography {

  private String bandcampURL;
  private BandcampAlbum[] albums;

  public BandcampDiscography(String bandcampURL) {
    this.bandcampURL = bandcampURL;
    this.albums = new BandcampAlbum[0];
  }


  public void addAlbum(BandcampAlbum newAlbum) {
    // Create new array to replace albums
    BandcampAlbum[] newAlbums = new BandcampAlbum[albums.length + 1];

    // populate newAlbums by using albums data
    for(int i = 0; i < albums.length; i++) {
      newAlbums[i] = albums[i];
    }

    // Add newAlbum to the end of newAlbums
    newAlbums[albums.length] = newAlbum;

    // Apply newAlbums to albums
    albums = newAlbums;
  }
}
