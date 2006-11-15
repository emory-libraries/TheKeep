class StaffName < ActiveRecord::Base
  has_one :Content
  
  
  def self.getStaff
    @staff = find(:all, :select => 'name, id', :order => 'name')
    
    names = []    
    for s in @staff
      names << [s.name, s.id]
    end  
    
    return names
  end
end
