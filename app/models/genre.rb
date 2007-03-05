class Genre < ActiveRecord::Base
  has_and_belongs_to_many :contents
  belongs_to :Authority
  
  validates_presence_of :genre
  validates_length_of :genre, :in => 1..255, :message => "Genre must be between 1 and 255 characters"
  
  def self.getGenres
    @genres = find(:all, :select => 'genre, id, authority_id', :order => 'genre')
    
    g = []    
    for genre in @genres
      a = Authority.find(genre.authority_id)
      g << [genre.genre + " [" + a.authority + "]", genre.id]
    end  
    
    return g
  end   
end
