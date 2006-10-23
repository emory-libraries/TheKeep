class Restriction < ActiveRecord::Base
  has_many :AccessRights
  
 
  def self.getRestrictions
    @restrictions = find(:all, :select => 'description, id', :order => 'description')
    
    r = []    
    for restriction in @restrictions
      r << [restriction.description, restriction.id]
    end  
    
    return r
  end  
end
