class Location < ActiveRecord::Base
  has_one :Content
  
  
  def self.getLocations
    @locations = find(:all, :select => 'name, id', :order => 'name')
    
    locs = []    
    for l in @locations
      locs << [l.name, l.id]
    end  
    
    return locs
  end
      
end
