class Target < ActiveRecord::Base
  has_one :TechImage
  
  def self.getTargets
    @targets = find(:all, :select => 'name, id', :order => 'name')
    
    t = []    
    for target in @targets
      t << [target.name, target.id]
    end  
    
    return t
  end
end
