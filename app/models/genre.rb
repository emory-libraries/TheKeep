class Genre < ActiveRecord::Base
  has_and_belongs_to_many :contents
  belongs_to :Authority
  
  
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
