class Role < ActiveRecord::Base
  has_many :names, :through => :ContentsNames
  
  def self.getRoles
    @roles = find(:all, :select => 'title, id', :order => 'title')
    
    r = []    
    for role in @roles
      r << [role.title, role.id]
    end  
    
    return r
  end  
end
