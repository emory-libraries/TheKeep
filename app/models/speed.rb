class Speed < ActiveRecord::Base

  def self.getSpeeds
    @speeds = find(:all, :select => 'speed, id', :order => 'speed')
    
    speed = []    
    for s in @speeds
      speed << [s.speed, s.id]
    end  
    
    return speed
  end
  
end
