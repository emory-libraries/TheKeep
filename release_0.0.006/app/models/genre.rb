class Genre < ActiveRecord::Base
  has_and_belongs_to_many :contents
  
  def self.getGenres
    @genres = find(:all, :select => 'genre, id', :order => 'genre')
    
    g = []    
    for genre in @genres
      g << [genre.genre, genre.id]
    end  
    
    return g
  end   
end
