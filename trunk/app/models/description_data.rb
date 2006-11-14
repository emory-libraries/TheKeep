class DescriptionData < ActiveRecord::Base
  has_one :Content


  def self.getMSSNumbers
    @dd = find(:all, :select => 'id, mss_number')
    
    mss = []    
    for d in @dd
      mss << [d.mss_number, d.id]
    end  
    
    return mss
  end
end
